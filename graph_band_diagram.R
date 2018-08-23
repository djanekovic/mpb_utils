#!/usr/bin/env Rscript

description="
This is helper script for printing mpb band gap data and plotting pretty
photonic band pictures. Under the hood, script is just a wrapper for ggplot2."


# program dobiva dvije .out datoteke, --tm= *_tm.out i --te=*_te.out (?)
# Opcije koje je moguce specificirati:
#	*broj bandova -> neka for petlja za dodavanje u ggplot
#	*size linije -> default 0.7
#	*boja tm -> default "red"
#	*boja te -> default "blue"
#	*shape_tm_point -> default je 0 (kvadratic)
#					-> ukoliko stavim <0 nista ostatak se mapira na geom_point
#	*shape_te_point -> cp shape_tm_point
# 	*nacrtaj i band_gap -> bool, default je true
#	*border -> forsiraj border na 0
#	*dim -> za sad je default 2

suppressPackageStartupMessages(library("optparse"))
suppressPackageStartupMessages(library("ggplot2"))
suppressPackageStartupMessages(library("magrittr"))
suppressPackageStartupMessages(library("stringr"))

option_list <- list(
make_option(c("-o", "--output"),
		action = "store",
		type = "character",
		default = "",
		help = "Filename to save graph."),
make_option(c("-v", "--verbose"),
		action = "store_true",
		default = FALSE,
		help = "Increase verbosity. Turn on to debug script."),
make_option(c("-b", "--border"),
		action="store_true",
		default=FALSE,
		help="Force axis to start at zero. By default axis start with small
		offset."),
make_option(c("-n", "--band_num"),
		type = "integer",
		default=1,
		# maybe print just what you have and on stderr
		# print that something is wrong
		help = "Specify number of bands on the plot. In case number is bigger
 	   	than number of bands in .out file maximum will be plotted. In that
 	   	case, user will see warning written out on stderr."),
# TODO: split maybe?
make_option(c("-s", "--size"),
		type="double",
		default=0.7,
		help="Specify line thickness on the graph. One option for TM and TE."),
make_option(c("--shape_tm_point"),
		type="integer",
		default=0,
		help="Specify point shape. Look geom_point shapes for details. In case
		-1 passed no geom_point shape. Default is 0."),
make_option(c("--shape_te_point"),
		type="integer",
		default=1,
		help="Specify point shape. Look geom_point shapes for details. In case
		-1 passed no geom_point shape. Default is 1."),
make_option(c("-g", "--band_gap"),
		action="store_true",
		default = FALSE,
		help="Plot band gaps."),
make_option(c("-d", "--dimension"),
		type="integer",
		default=2,
		help="Problem dimensionality. Program now supports just 2D problems.")
)

epilogue <- "
This script has quite a few arguments. Fear not! Usage is actually pretty simple.
I hope it is... I made this tool to be simple and easy. Arguments are here to
make graphs more flexible without going into R code and chaning it yourself.

EXAMPLES
---------

To begin with, you need to have tm.out and te.out files. This script lives
under the assumption that you want to plot both TE and TM.

* to generate plot.png plot of both TE and TM modes:
$ Rscript graph_band_diagram.R square_tm.out square_te.out -o plot.png
 -- plot.png has only one band and no bands are plotted.

* to generate plot.pdf of both TE, TM and band gaps:
$ Rscript graph_band_diagram.R square_tm.out square_te.out -g -o plot.pdf

* to generate plot.pdf of both 8 TE, TM bands and band gaps:
$ Rscript graph_band_diagram.R square_tm.out square_te.out -g -n 8 -o plot.pdf
"

parser <- OptionParser(usage = "%prog -o outputfile [options] tm.out te.out",
					   option_list = option_list,
					   description = description,
					   epilogue = epilogue)
arguments <- parse_args(parser, positional_arguments=2)

args <- arguments$options
files <- arguments$args

no_output_name_msg <- "You should really set output argument... I am setting
output name to plot.png"

if (args$output == "") {
	if (args$verbose) print (no_output_name_msg)
	args$output = "plot.png"
}

read_tm_msg = paste("You passed tm.out as ", files[1], sep='')
if (args$verbose) print (read_tm_msg)
if (args$verbose) print ("Reading...")
tm <- readLines(files[1])
grep (pattern = "tmfreq", x = tm, value = TRUE) %>% read.csv(text = ., sep = ',') -> tmfreq_data
grep (pattern = "Gap from", tm, value = TRUE) %>% str_match(pattern = "\\((.*?)\\).*\\((.*?)\\)") %>% '['(, 2:3) -> tm_gap_data

if (args$verbose) print ("Done reading")

read_te_msg = paste("You passed tm.out as ", files[2], sep='')
if (args$verbose) print (read_te_msg)
if (args$verbose) print ("Reading...")

te <- readLines(files[2])
grep (pattern = "tefreq", x = te, value = TRUE) %>% read.csv(text = ., sep = ',') -> tefreq_data
grep (pattern = "Gap from", te, value = TRUE) %>% str_match(pattern = "\\((.*?)\\).*\\((.*?)\\)") %>% '['(, 2:3) -> te_gap_data

if (args$verbose) print ("Done reading")

g <- ggplot(data = tmfreq_data, aes(x = k.index))

band_num_msg <- paste("Plotting", args$band_num, "bands")
if (args$band_num) print (band_num_msg)

# TODO: check somehow if there are enought bands and default to max
for (i in seq(args$band_num)) {
	g <- g + geom_line(data = tmfreq_data,
                   	   aes_string(y = paste("tm.band.", i, sep = '')),
                   	   color = "red",
                   	   size = args$size)
}

for (i in seq(args$band_num)) {
	g <- g + geom_line(data = tefreq_data,
                   	   aes_string(y = paste("te.band.", i, sep = '')),
                   	   color = "blue",
                   	   size = args$size)
}

if (args$band_gap) {
	band_gap_msg <- "Plotting available band gaps"
} else {
	band_gap_msg <- "Not plotting band gaps"
}

if (args$verbose) print (band_gap_msg)

if (args$band_gap) {
	for (i in seq(dim(te_gap_data)[1])) {
		g <- g + geom_rect(aes_string(ymin=te_gap_data[i, 1],
                       	   	   	  	  ymax=te_gap_data[i, 2],
                       	   	   	  	  xmax=max(tmfreq_data$k.index),
                       	   	   	  	  xmin=min(tmfreq_data$k.index)),
                   	   	   alpha=0.005,
                   	   	   fill="blue")
	}

	for (i in seq(dim(tm_gap_data)[1])) {
		g <- g + geom_rect(aes_string(ymin=tm_gap_data[i, 1],
                       	   		  	  ymax=tm_gap_data[i, 2],
                       	   		  	  xmax=max(tmfreq_data$k.index),
                       	   		  	  xmin=min(tmfreq_data$k.index)),
                   	   	   alpha=0.005,
                   	   	   fill="red")
	}
}

if (args$verbose) {
	print (paste("Outputing plot named as", args$output))
}

ggsave(args$output)

if (args$verbose) print ("Plot saved, goodbye world!")
