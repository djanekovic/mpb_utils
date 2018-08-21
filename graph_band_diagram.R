#!/usr/bin/env Rscript

description="
This is helper script for printing mpb band gap data and plotting pretty
photonic band pictures. Under the hood, script is just a wrapper for ggplot2."


# --> REMOVE LATER
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

# TODO: make program parse two files but figure out how to pipe and grep
# during python is running. Script has to load some sort of csv.
# Parsing 2 files is just too painful

suppressPackageStartupMessages(library("optparse"))
suppressPackageStartupMessages(library("ggplot2"))

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


parser <- OptionParser(usage = "%prog -o outputfile [options] tm.csv te.csv",
					   option_list = option_list,
					   description = description,
					   epilogue = epilogue)
arguments <- parse_args(parser, positional_arguments=2)

print (arguments)
if (length(arguments$output) == 0) {
	print ("This is obligatory argument, without it script wont work!")
	# TODO: end in a R way
	return (1)
}

# NOTE: this is just a test, I need to figure out how to read or parse .out and create .csv
tmfreq <- read.csv("~/photonic_crystals/models/output/square_tm.csv")
tefreq <- read.csv("~/photonic_crystals/models/output/square_te.csv")

g <- ggplot(data=tmfreq, aes(x=k.index))

# TODO: this should work
#for (i in seq(8)) {
#  paste("tm.band.", i, sep = '') %>% g + geom_line(aes(y=.) -> g
#}

g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.1),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.2),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.3),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.4),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.5),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.6),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.7),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tmfreq,
                   aes(y=tm.band.8),
                   color="red",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.1),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.2),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.3),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.4),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.5),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.6),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.7),
                   color="blue",
                   size=0.7)
g <- g + geom_line(data=tefreq,
                   aes(y=te.band.8),
                   color="blue",
                   size=0.7)

# TODO: because of this I should read .out file (not so bad but i need to figure out how to parse .out and create .csv in R
# or user should have an option to enter bandgaps to print (pretty bad and should be plan B)
g <- g + geom_rect(aes(ymin=0.5931405182468739,
                       ymax=0.5931535893552192,
                       xmax=max(tmfreq$k.index),
                       xmin=min(tmfreq$k.index)),
                   alpha=0.005,
                   fill="blue")

g <- g + geom_rect(aes(ymin=0.8096891662050553,
                       ymax=0.824181449220372,
                       xmax=max(tmfreq$k.index),
                       xmin=min(tmfreq$k.index)),
                   alpha=0.005,
                   fill="blue")

g <- g + geom_rect(aes(ymin=1.0860733987620035,
                       ymax=1.087869087137856,
                       xmax=max(tmfreq$k.index),
                       xmin=min(tmfreq$k.index)),
                   alpha=0.005,
                   fill="blue")

g <- g + geom_rect(aes(ymin=0.28094795584045934,
                       ymax=0.4171142494115699,
                       xmax=max(tmfreq$k.index),
                       xmin=min(tmfreq$k.index)),
                   alpha=0.005,
                   fill="red")

g <- g + geom_rect(aes(ymin=0.7133951517520881,
                       ymax=0.7413109658608329,
                       xmax=max(tmfreq$k.index),
                       xmin=min(tmfreq$k.index)),
                   alpha=0.005,
                   fill="red")
# TODO: theme, labels, ticks -> need to google those things
g <- g + theme_classic()
