#!/usr/bin/env Rscript

description="
This is helper script for printing mpb band gap data and plotting pretty
photonic band pictures. Under the hood, script is just a wrapper for ggplot2."


# program dobiva dvije .out datoteke, --tm= *_tm.out i --te=*_te.out (?)
# Nisam siguran zato sto mi mozda treba i samo ms.run() za total band gap
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
		default = TRUE,
		help="Plot geom_rect where band_gap is."),
make_option(c("-d", "--dimension"),
		type="integer",
		default=2,
		help="Problem dimensionality. Program now supports just 2D problems.")
)

# TODO: finish epilogue
epilogue <- "
This script has quite a few arguments. Fear not! Usage is actually pretty simple.
I hope it is... I made this tool to be simple and easy. Arguments are here to
make graphs more flexible without going into R code and chaning it yourself.

EXAMPLES
---------"


parser <- OptionParser(usage = "%prog -o outputfile [options] tm.out te.out",
					   option_list = option_list,
					   description = description,
					   epilogue = epilogue)
arguments <- parse_args(parser, positional_arguments=2)

# TODO: test if output file is here
if (arguments$options$output == "") {
	print ("You need to pass output argument")
	# TODO: end in a R way
	return (1)
}

tm <- readLines(arguments$args[1])
grep (pattern = "tmfreq", x = tm, value = TRUE) %>% read.csv(text = ., sep = ',') -> tmfreq_data
grep (pattern = "Gap from", tm, value = TRUE) %>% str_match(pattern = "\\((.*?)\\).*\\((.*?)\\)") %>% '['(, 2:3) -> tm_gap_data

te <- readLines(arguments$args[2])
grep (pattern = "tefreq", x = te, value = TRUE) %>% read.csv(text = ., sep = ',') -> tefreq_data
te_gap_data <- grep (pattern = "Gap from", te, value = TRUE) %>% str_match(pattern = "\\((.*?)\\).*\\((.*?)\\)") %>% '['(, 2:3)

g <- ggplot(data = tmfreq_data, aes(x = k.index))

for (i in seq(8)) {
	g <- g + geom_line(data = tmfreq_data,
                   	   aes_string(y = paste("tm.band.", i, sep = '')),
                   	   color = "red",
                   	   size = arguments$options$size)
}

for (i in seq(8)) {
	g <- g + geom_line(data = tefreq_data,
                   	   aes_string(y = paste("te.band.", i, sep = '')),
                   	   color = "blue",
                   	   size = arguments$options$size)
}

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

ggsave(arguments$options$output)
