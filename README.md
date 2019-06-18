# ProtPred Framework
The ProtPred Framework is a python framework for testing protein function prediction under varying fractions of missing protein annotation.
The framework uses a command-line interface in which the user is able to specify a lot of different prediction parameters.
The framework allows for different prediction methods to be implemented. These methods can be specified by the user in the command-line interface. 
The ProtPred Framework takes proteomes and Gene Ontology annotations as input and outputs a prediction performance plot showing how
the chosen prediction performs under varying amounts of missing annotation data.

## Gene Function Prediction with Missing Data
The ProtPred Framework has been built for the Gene Function Prediction with Missing Data Project at TU Delft by 3rd year
bioinformatics students from Hogeschool Leiden.

## Implemented protein prediction methods
A BLAST-based protein prediciton method which couples the annotation from the best BLAST-hit of a protein in one organism to the BLAST query protein
which has no annotation (BLAST-tophit). A similar method taking the annotation from the 20 best hits of a protein has also been implemented. (BLAST-top20)
Thirdly, a variation on the BLAST-tophit method has been implemented which discards proteins for which there is no annotation.

## Python packages required by the framework
The following packages are required in order to run the ProtPred Framework:
* Numpy (v1.16.2)
* Matplotlib (v2.2.4)
* Pandas (v0.24.2)
* Scikit-learn (v0.20.3)
* Scipy (v1.2.1)

## Input required by the framework
The following input files are required in order to run the ProtPred Framework:
* traindata : A file containing the file the prediction method uses to make predictions (in a BLAST-method, this would be the BLAST-results (query, hits))
* traingaf : A Gene Ontology annotation file containing annotation for the proteins in the traindata-file.
* testdata : A proteome file which should containing proteins the prediction methods should predict the annotation for.
* testgaf : A Gene Ontology annotation file containing annotation for the proteome in the testdata-file.

Files need to be put into the files directory and will be specified as 'files/**_filename_**'

### Example of input data
For testing the framework we used the proteomes and GO-annotation from Mouse and Rat:
* traindata : _blast_besthit_traindata_mouserat_

This file contains rows consisting of a query protein-id followed by the best blast hit protein-id. 

* traingaf : _goa_rat.gaf_

This file contains Gene Ontology annotations for the proteome of Rat.
* testdata : _blast_besthit_testdata_mouse_

This file contains all the protein-id's present in Mouse (one protein in each row)
* testgaf : _goa_mouse.gaf_

This file contains Gene Ontology annotations for the proteome of Mouse.

## Specifiable parameters in the framework
The user is able to specify the following options as arguments in the command line interface of the framework:
* -p or --predictor (Predictor script to use, default: blast)
* -e or --evaluator (Evaluator metric to use, default: f-score)
* -l or --plotter (Type of plotter to use, default: line)
* -s or --stepsize (Missing data fraction step-size to use, default: 5)
* -E or --evidence (Annotation evidence codes to use, default: tuple of all, these need to be comma-seperated)
* -t or --traindata (Training data to use, must be specified)
* -g or --testgaf (Test annotation to use, must be specified)
* -d or --domains (Annotation domains to use, default: tuple of all, these need to be comma-seperated)
* -r or --repeats (Amount of repeats for each missing data fraction, default: 1)
* -n or --threads (Amount of threads to use, default: all threads available)
* -f or --nogofix (Whether to not add parent GO-terms to the annotation, default: False)
* -a or --predargs (Extra arguments to give to the Predictor, these need to be comma-seperated)
* -P or --plst (The amount of PLST-dimensions to use, when using -1, PLST is disabled, default: -1)
* -A or --argfile (A config file to give to the framework, default: None)
* -h or --plotheader (A title for the prediction performance plot, default: Plot Title)
* -c or --color (Color for the line in the performance plot, default: tuple of all)
* -L or --linetype (Linetype to use in the performance plot, default: tuple of all)
* -h or --help (Display help)

### Example of using different parameters

As an example, the following bash code would run the Framework with a BLAST-tophit prediction method and
predict the annotation of mouse proteins based on rat annotation. The user wants to see the f-score and precision scores
in the performance plot which the framework builds. As a stepsize for the fractions of missing data a size of 5 was chosen.
Also, to look at the deviation between different annotation samples, the user wants to have each fraction repeated five times.
Lastly, in order to speed up the prediction process, the user wants to use 4 threads.
```bash
python3 protpred.py -t files/blast_besthit_traindata_mouserat -g files/goa_rat.gaf -T files/blast_besthit_testdata_mouse -G files/goa_mouse.gaf -p predictors/pred_blast_besthit.py -e f-score,precision -s 5 -r 5 -n 4
```

## User-specifiable prediction methods
A user of the framework can add different prediciton methods to the framework, by adding a python-script containing a _Predictior_ class to the
_predictors_ directory in the framework. The prediction method can then by specified by using the _-p_ command line argument, as is shown
in the parameter example. If additional files are required by the predictor these files can be given to the predictor script using
the argfile argument in the command line: _-a_. Files specified by the argfile argument will directly be given to the predictor class in the python-script.

## Usage of a config-file
As an easy way to compare multiple different framework runs with each other, a config file can be used. In this file, the same arguments as in the regular command-line can be used. The top row of
the file should containg the title of the plot which will contain all the framework runs. The rows below should contain the options for the runs itself, using the same arguments as in the command-line.

### Example of a config-file
As an example, the following config file would result in a plot titled _Blastmethod comparison domain F_ which draws
a line for the BLAST-tophit prediction method, the BLAST-top20 method and the BLAST-tophit only using annotated proteins using
annotation in the Molecular Function Gene Ontology domain.

```
Title: Blastmethod comparison domain F
TopBlast: --stepsize 5 --traindata ./files/blast_besthit_traindata_mouserat --traingaf ./files/goa_rat.gaf --testdata ./files/blast_besthit_testdata_mouse --testgaf ./files/goa_mouse.gaf --predictor predictors/blast.py --evaluator average_precision --predargs 1,false --evidence EXP,IDA,IPI,IMP,IGI,IEP,HTP,HTP,HDA,HMP,HGI,HEP,IBA,IBD,IKR,IRD,ISS,ISO,ISA,ISM,IGC,RCA,TAS,NAS,IC,ND,IEA,IEA --domain F --repeats 1 --threads 3 
20Blast: --stepsize 5 --traindata ./files/blast_top20_traindata_mouserat --traingaf ./files/goa_rat.gaf --testdata ./files/blast_top20_testdata_mouse --testgaf ./files/goa_mouse.gaf --predictor predictors/blast.py --evaluator average_precision --predargs 20,false --evidence EXP,IDA,IPI,IMP,IGI,IEP,HTP,HTP,HDA,HMP,HGI,HEP,IBA,IBD,IKR,IRD,ISS,ISO,ISA,ISM,IGC,RCA,TAS,NAS,IC,ND,IEA,IEA --domain F --repeats 1 --threads 3
Annotated: --stepsize 5 --traindata ./files/blast_onlyannotated_traindata_rat --traingaf ./files/goa_rat.gaf --testdata ./files/blast_onlyannotated_testdata_mouse --testgaf ./files/goa_mouse.gaf --predictor predictors/blast.py --evaluator average_precision --predargs 1,true --evidence EXP,IDA,IPI,IMP,IGI,IEP,HTP,HTP,HDA,HMP,HGI,HEP,IBA,IBD,IKR,IRD,ISS,ISO,ISA,ISM,IGC,RCA,TAS,NAS,IC,ND,IEA,IEA --domain F --repeats 1 --threads 3
```

The config file can be specified in the following command line argument: _--argfile_
An example is shown below:
```bash
python3 protpred.py --argfile config.txt
```
### Example of a framework run resulting in a perfomance plot
A run using the config file below will result in the plot shown further below:


Config (go_fix_domain_c.txt):
```
Title: Tophit-BLAST with and without adding GO-parents (Domain C)
topBLAST with gofix: --stepsize 5 --traindata ./files/blast_besthit_traindata_mouserat --traingaf ./files/goa_rat.gaf --testdata ./files/blast_besthit_testdata_mouse --testgaf ./files/goa_mouse.gaf --predictor predictors/blast.py --evaluator f-score --predargs 1,false --evidence EXP,IDA,IPI,IMP,IGI,IEP,HTP,HTP,HDA,HMP,HGI,HEP,IBA,IBD,IKR,IRD,ISS,ISO,ISA,ISM,IGC,RCA,TAS,NAS,IC,ND,IEA,IEA --domain C --repeats 10 --threads 1 
topBLAST without gofix: --stepsize 5 --traindata ./files/blast_beshit_traindata_mouserat --traingaf ./files/goa_rat.gaf --testdata ./files/blast_beshit_testdata_mouse --testgaf ./files/goa_mouse.gaf --predictor predictors/blast.py --evaluator f-score --predargs 1,false --evidence EXP,IDA,IPI,IMP,IGI,IEP,HTP,HTP,HDA,HMP,HGI,HEP,IBA,IBD,IKR,IRD,ISS,ISO,ISA,ISM,IGC,RCA,TAS,NAS,IC,ND,IEA,IEA --domain C --repeats 10 --threads 1 --nogofix
```
Calling the framework using this config:
```bash
python3 protpred.py --argfile go_fix_domain_c.txt
```
Resulting plot:
![alt text](https://github.com/Sbrussee/GenePredMissData/blob/master/sample_plot.png)
