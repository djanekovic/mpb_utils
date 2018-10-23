seminar: seminar.tex literatura.bib
	pdflatex seminar.tex
	bibtex seminar.aux
	pdflatex seminar.tex
	pdflatex seminar.tex

prezentacija: prezentacija.tex
	pdflatex prezentacija.tex && pdflatex prezentacija.tex

clean:
	rm seminar.aux
	rm seminar.bbl
	rm seminar.bcf
	rm seminar.blg
	rm seminar.log
	rm seminar.out
	rm seminar.run.xml
	rm seminar.toc
