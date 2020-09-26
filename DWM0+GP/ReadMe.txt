How to run the Python Recursive Entropy Program

1) download the files in this directory to the same folder on your PC
2) run the notebook RecursiveEntropyBitBucket.ipynb in your Python environment
3) To run a sample, adjust the settings in top-level driver of the Python code
The code is already preset for sample S2.txt
sourceFileName = #name of sample to run (S1.txt through S18.txt)
beta = #blocking frequency threshold
sigma = #stop word frequency threshold
mu = #match threshold
muIncrement = #amount to increase match threshold each iteration
epsilon = #entropy threshold
epsilonIncrement = #amount increase entropy threshold each iteration
runClusterMetrics = #if True, will let you compare actual F-meas of each cluster 
	with its entropy value, but slows run time
runFinalMetrics = #if True, will give F-meas of final result
createFinalJoin = #if True, will append cluster IDs to original input file in the format
	refID:clusterID:original record

Running metrics will only work when the sample has a truth file (annotations) compatible with
	the "er-metrics.jar" program
All of the provided samples S1 to S18 have a truth file
If you run your own sample data with a truth file 
	set "runClustersMetrics = False" and "runFinalMetrics = False"

If running your own samples, be sure
1) Set "runClustersMetrics = False" and "runFinalMetrics = False"
2) Ref items are all delimited with blank, comma, pipe, or some other non-word character
3) The first row in sample is a header row, otherwise you will lose the first reference
4) The first item in each reference must be a unique reference identifier (RefID) 
5) The RefID must comprise only uppercase letters and digits
6) Run times are primarily a function of beta (blocking) setting, 
	the larger beta, the longer the run time

If running the provided samples, here are some settings and their results
Also set "runFinalMetrics = True" to see your results
Sample	Size	DQ	Mixed	MuStart	MuFinal	Beta	Sigma	Epsilon	Prec	Recall	F-meas										Precision	Recall	F-Measure
S1	50	Good	No	0.50	0.70	6	7	4.2	0.9630	0.9630	0.9630
S2	100	Good	No	0.50	0.80	6	7	4.3	0.8936	0.8750	0.8842
S3	868	Good	No	0.50	1.00	9	95	4.5	0.9123	0.9286	0.9204
S4	1,912	Good	No	0.50	0.90	12	22	4.2	0.9333	0.8899	0.9111
S5	3,004	Good	No	0.50	1.00	12	53	4.1	0.9435	0.8867	0.9142
S6	19,998	Good	No	0.50	0.90	35	403	15.1	0.9457	0.9737	0.9595
S7	3,000	Good	Yes	0.50	1.00	14	24	3	0.9464	0.8665	0.9047
S8	1,000	Poor	No	0.50	0.60	7	15	35	0.5640	0.5269	0.5448
S9	1,000	Poor	No	0.50	0.50	14	16	35	0.5165	0.3282	0.4014
S10	2,000	Poor	Yes	0.50	0.60	10	15	35	0.5774	0.4092	0.4790
S11	4,000	Poor	Yes	0.50	0.60	10	16	36	0.5608	0.39657	0.4646
S12	6,000	Poor	Yes	0.50	0.70	10	16	34	0.59957	0.36336	0.4525
S13	2,000	Good	Yes	0.50	0.90	12	40	5.8	0.92272	0.8394	0.8791
S14	5,000	Good	Yes	0.50	0.90	15	125	5.7	0.92730	0.8600	0.8924
S15	10,000	Good	Yes	0.50	1.00	20	90	5.9	0.93018	0.8108	0.8664
S16	2,000	Poor	Yes	0.50	0.60	13	30	34	0.60598	0.4766	0.5335
S17	5,000	Poor	Yes	0.50	0.70	13	25	36	0.54182	0.4312	0.4802
S18	10,000	Poor	Yes	0.50	0.70	15	23	37	0.56018	0.3686	0.4446



