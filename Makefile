#Stephen Stengel <stephen.stengel@cwu.edu> 40819903
#makefile for Project 2

#Don't need to compile anything for this


#Miscellaneous
.PHONY: clean
clean:
	rm -f 565-project2-stephen-stengel.zip

.PHONY: backup
backup:
	ssh-backup-pi | lolcat

.PHONY: zip
zip:
	7z a -mx=9 565-project2-stephen-stengel.zip Makefile \
			gold-getter.py README LICENSE images/

.PHONY: script
script:
	make clean && make && make zip && make backup
