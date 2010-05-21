# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 

include $(MOABASE)/template/moa/prepare.mk

moa_id = soapdb
template_title = Bowtie index builder
template_description = Builds a bowtie index from a reference sequence

#########################################################################
# Prerequisite testing
moa_prereq_simple += bowtie-build

moa_must_define += soapdb_input
soapdb_input_help = Input fasta file to build a SOAP bwt database from
soapdb_input_type = file

include $(MOABASE)/template/moa/core.mk

soapdb: 
	2bwt-builder $(soapdb_input)

#one of the database files
$(soapdb_name).1.ebwt: $(soapdb_input_files)
	-$e rm -f $(soapdb_name).*.ebwt
	$e bowtie-build $(call merge,$(comma),$^) $(soapdb_name)
	touch $(soapdb_name)

soapdb_clean:
	-rm -f $(soapdb_name).*.ebwt
