#!/usr/bin/env Rscript

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

option_list <- list(
					make_option(c("-v", "--verbose"),
								action = "store_true",
								default = FALSE,
								help = "Increase verbosity.
								Turn on to debug script."),
					make_option(c("-b", "--border"),
								action="store_true",
								default=FALSE,
								help="Force axis to start at zero.
								By default axis start with small offset."),
					make_option(c("-n", "--band_num"),
								type = "integer",
								default=1,
								# maybe print just what you have and on stderr
								# print that something is wrong
								help = "Specify number of bands on the plot.
								In case number is bigger than number
								of bands in .out file, error will be generated
								and script will exit (?)"),
					make_option(c("-s", "--size"),
								type="double",
								default=0.7,
								help="Specify line thickness on the graph.
								One option for TM and TE."),
					make_option(c("--shape_tm_point"),
								type=integer,
								default=0,
								help="Specify point shape.
								Look geom_point shapes for details.
								In case -1 passed no geom_point shape.
								Default is 0."),
					make_option(c("--shape_te_point"),
								type=integer,
								default=1,
								help="Specify point shape.
								Look geom_point shapes for details.
								In case -1 passed no geom_point shape.
								Default is 1."),
					make_option(c("-g", "--band_gap"),
								action="store_true",
								default = TRUE,
								help="Plot geom_rect where band_gap is."),
					make_option(c("-d", "--dimension"),
								type=integer,
								default=2.
								help="Problem dimensionality.
								Program now supports just 2D problems."))

parser <- OptionParser(usage="%prog [options] tm.out te.out full.out
