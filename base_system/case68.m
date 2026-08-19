function mpc = case68
%CASEIEEE68
%    06/15/20 PSAT ARCHIVE         100.00 2020 S 68-Bus 83-Line System                                                              
%
%   Converted by MATPOWER 6.0 using CDF2MPC on 15-Jun-2020
%   from 'C:\Users\Timon\myPSAT\psat\filters\d_IEEE68bus.cf'.
%
%   WARNINGS:
%       check the title format in the first line of the cdf file.
%       MVA limit of branch 1 - 54 not given, set to 0
%       MVA limit of branch 2 - 58 not given, set to 0
%       MVA limit of branch 3 - 62 not given, set to 0
%       MVA limit of branch 4 - 19 not given, set to 0
%       MVA limit of branch 5 - 20 not given, set to 0
%       MVA limit of branch 6 - 22 not given, set to 0
%       MVA limit of branch 7 - 23 not given, set to 0
%       MVA limit of branch 8 - 25 not given, set to 0
%       MVA limit of branch 9 - 29 not given, set to 0
%       MVA limit of branch 10 - 31 not given, set to 0
%       MVA limit of branch 11 - 32 not given, set to 0
%       MVA limit of branch 12 - 36 not given, set to 0
%       MVA limit of branch 13 - 17 not given, set to 0
%       MVA limit of branch 14 - 41 not given, set to 0
%       MVA limit of branch 15 - 42 not given, set to 0
%       MVA limit of branch 16 - 18 not given, set to 0
%       MVA limit of branch 17 - 36 not given, set to 0
%       MVA limit of branch 18 - 49 not given, set to 0
%       MVA limit of branch 18 - 50 not given, set to 0
%       MVA limit of branch 19 - 68 not given, set to 0
%       MVA limit of branch 20 - 19 not given, set to 0
%       MVA limit of branch 21 - 68 not given, set to 0
%       MVA limit of branch 22 - 21 not given, set to 0
%       MVA limit of branch 23 - 22 not given, set to 0
%       MVA limit of branch 24 - 23 not given, set to 0
%       MVA limit of branch 24 - 68 not given, set to 0
%       MVA limit of branch 25 - 54 not given, set to 0
%       MVA limit of branch 26 - 25 not given, set to 0
%       MVA limit of branch 27 - 37 not given, set to 0
%       MVA limit of branch 27 - 26 not given, set to 0
%       MVA limit of branch 28 - 26 not given, set to 0
%       MVA limit of branch 29 - 26 not given, set to 0
%       MVA limit of branch 29 - 28 not given, set to 0
%       MVA limit of branch 30 - 53 not given, set to 0
%       MVA limit of branch 30 - 61 not given, set to 0
%       MVA limit of branch 31 - 30 not given, set to 0
%       MVA limit of branch 31 - 53 not given, set to 0
%       MVA limit of branch 32 - 30 not given, set to 0
%       MVA limit of branch 33 - 32 not given, set to 0
%       MVA limit of branch 34 - 33 not given, set to 0
%       MVA limit of branch 34 - 35 not given, set to 0
%       MVA limit of branch 36 - 34 not given, set to 0
%       MVA limit of branch 36 - 61 not given, set to 0
%       MVA limit of branch 37 - 68 not given, set to 0
%       MVA limit of branch 38 - 31 not given, set to 0
%       MVA limit of branch 38 - 33 not given, set to 0
%       MVA limit of branch 40 - 41 not given, set to 0
%       MVA limit of branch 40 - 48 not given, set to 0
%       MVA limit of branch 41 - 42 not given, set to 0
%       MVA limit of branch 42 - 18 not given, set to 0
%       MVA limit of branch 43 - 17 not given, set to 0
%       MVA limit of branch 44 - 39 not given, set to 0
%       MVA limit of branch 44 - 43 not given, set to 0
%       MVA limit of branch 45 - 35 not given, set to 0
%       MVA limit of branch 45 - 39 not given, set to 0
%       MVA limit of branch 45 - 44 not given, set to 0
%       MVA limit of branch 46 - 38 not given, set to 0
%       MVA limit of branch 47 - 53 not given, set to 0
%       MVA limit of branch 48 - 47 not given, set to 0
%       MVA limit of branch 49 - 46 not given, set to 0
%       MVA limit of branch 51 - 45 not given, set to 0
%       MVA limit of branch 51 - 50 not given, set to 0
%       MVA limit of branch 52 - 37 not given, set to 0
%       MVA limit of branch 52 - 55 not given, set to 0
%       MVA limit of branch 54 - 53 not given, set to 0
%       MVA limit of branch 55 - 54 not given, set to 0
%       MVA limit of branch 56 - 55 not given, set to 0
%       MVA limit of branch 57 - 56 not given, set to 0
%       MVA limit of branch 58 - 57 not given, set to 0
%       MVA limit of branch 59 - 58 not given, set to 0
%       MVA limit of branch 60 - 57 not given, set to 0
%       MVA limit of branch 60 - 59 not given, set to 0
%       MVA limit of branch 61 - 60 not given, set to 0
%       MVA limit of branch 63 - 58 not given, set to 0
%       MVA limit of branch 63 - 62 not given, set to 0
%       MVA limit of branch 63 - 64 not given, set to 0
%       MVA limit of branch 65 - 62 not given, set to 0
%       MVA limit of branch 65 - 64 not given, set to 0
%       MVA limit of branch 66 - 56 not given, set to 0
%       MVA limit of branch 66 - 65 not given, set to 0
%       MVA limit of branch 67 - 66 not given, set to 0
%       MVA limit of branch 68 - 67 not given, set to 0
%       MVA limit of branch 27 - 53 not given, set to 0
%
%   See CASEFORMAT for details on the MATPOWER case file format.

%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 100;

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [
	1	2	0	0	5	100	1	1.045	0	1	0	1.06	0.94;
	2	2	0	0	10	100	1	0.98	0	1	0	1.06	0.94;
	3	2	0	0	9	100	1	0.983	0	1	0	1.06	0.94;
	4	2	0	0	7	1	1	0.997	0	1	0	1.06	0.94;
	5	2	0	0	10	100	1	1.011	0	1	0	1.06	0.94;
	6	2	0	0	8	100	1	1.05	0	1	0	1.06	0.94;
	7	2	0	0	8	100	1	1.063	0	1	0	1.06	0.94;
	8	2	0	0	9	100	1	1.03	0	1	0	1.06	0.94;
	9	2	0	0	9	100	1	1.025	0	1	0	1.06	0.94;
	10	2	0	0	8	100	1	1.01	0	1	0	1.06	0.94;
	11	2	0	0	7.2	100	1	1	0	1	0	1.06	0.94;
	12	2	0	0	5	100	1	1.0156	0	1	0	1.06	0.94;
	13	2	0	0	12	100	1	1.011	0	1	0	1.06	0.94;
	14	2	0	0	6.9	100	1	1	0	1	0	1.06	0.94;
	15	2	0	0	6.9	100	1	1	0	1	0	1.06	0.94;
	16	3	0	0	16.5	100	1	1	0	1	0	1.06	0.94;
	17	1	6000	300	0	0	1	1	0	1	0	1.06	0.94;
	18	1	2470	123	0	0	1	1	0	1	0	1.06	0.94;
	19	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	20	1	680	103	0	0	1	1	0	1	0	1.06	0.94;
	21	1	274	115	0	0	1	1	0	1	0	1.06	0.94;
	22	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	23	1	248	85	0	0	1	1	0	1	0	1.06	0.94;
	24	1	309	-92	0	0	1	1	0	1	0	1.06	0.94;
	25	1	224	47	0	0	1	1	0	1	0	1.06	0.94;
	26	1	139	17	0	0	1	1	0	1	0	1.06	0.94;
	27	1	281	76	0	0	1	1	0	1	0	1.06	0.94;
	28	1	206	28	0	0	1	1	0	1	0	1.06	0.94;
	29	1	284	27	0	0	1	1	0	1	0	1.06	0.94;
	30	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	31	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	32	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	33	1	112	0	0	0	1	1	0	1	0	1.06	0.94;
	34	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	35	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	36	1	102	-19.46	0	0	1	1	0	1	0	1.06	0.94;
	37	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	38	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	39	1	267	12.6	0	0	1	1	0	1	0	1.06	0.94;
	40	1	65.63	23.53	0	0	1	1	0	1	0	1.06	0.94;
	41	1	1000	250	0	0	1	1	0	1	0	1.06	0.94;
	42	1	1150	250	0	0	1	1	0	1	0	1.06	0.94;
	43	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	44	1	267.55	4.84	0	0	1	1	0	1	0	1.06	0.94;
	45	1	208	21	0	0	1	1	0	1	0	1.06	0.94;
	46	1	150.7	28.5	0	0	1	1	0	1	0	1.06	0.94;
	47	1	203.12	32.59	0	0	1	1	0	1	0	1.06	0.94;
	48	1	241.2	2.2	0	0	1	1	0	1	0	1.06	0.94;
	49	1	164	29	0	0	1	1	0	1	0	1.06	0.94;
	50	1	100	-147	0	0	1	1	0	1	0	1.06	0.94;
	51	1	337	-122	0	0	1	1	0	1	0	1.06	0.94;
	52	1	158	30	0	0	1	1	0	1	0	1.06	0.94;
	53	1	252.7	118.56	0	0	1	1	0	1	0	1.06	0.94;
	54	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	55	1	322	2	0	0	1	1	0	1	0	1.06	0.94;
	56	1	200	73.6	0	0	1	1	0	1	0	1.06	0.94;
	57	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	58	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	59	1	234	84	0	0	1	1	0	1	0	1.06	0.94;
	60	1	208.8	70.8	0	0	1	1	0	1	0	1.06	0.94;
	61	1	104	125	0	0	1	1	0	1	0	1.06	0.94;
	62	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	63	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	64	1	9	88	0	0	1	1	0	1	0	1.06	0.94;
	65	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	66	1	0	0	0	0	1	1	0	1	0	1.06	0.94;
	67	1	320	153	0	0	1	1	0	1	0	1.06	0.94;
	68	1	329	32	0	0	1	1	0	1	0	1.06	0.94;
];

%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf
mpc.gen = [
	1	250     0	9999	-9999	1.045	100	1	350     0	0	0	0	0	0	0	0	0	0	0	0;
	2	545     0	9999	-9999	0.98	100	1	645     0	0	0	0	0	0	0	0	0	0	0	0;
	3	650     0	9999	-9999	0.983	100	1	750     0	0	0	0	0	0	0	0	0	0	0	0;
	4	632     0	9999	-9999	0.997	100	1	732     0	0	0	0	0	0	0	0	0	0	0	0;
	5	505     0	9999	-9999	1.011	100	1	605     0	0	0	0	0	0	0	0	0	0	0	0;
	6	700     0	9999	-9999	1.05	100	1	800     0	0	0	0	0	0	0	0	0	0	0	0;
	7	560     0	9999	-9999	1.063	100	1	660     0	0	0	0	0	0	0	0	0	0	0	0;
	8	540     0	9999	-9999	1.03	100	1	640     0	0	0	0	0	0	0	0	0	0	0	0;
	9	800     0	9999	-9999	1.025	100	1	900     0	0	0	0	0	0	0	0	0	0	0	0;
	10	500     0	9999	-9999	1.01	100	1	600     0	0	0	0	0	0	0	0	0	0	0	0;
	11	1000	0   9999	-9999	1       100	1	1100	0	0	0	0	0	0	0	0	0	0	0	0;
	12	1350	0   9999	-9999	1.0156	100	1	1450	0	0	0	0	0	0	0	0	0	0	0	0;
	13	3591	0   9999	-9999	1.011	100	1	3691	0	0	0	0	0	0	0	0	0	0	0	0;
	14	1785	0   9999	-9999	1       100	1	1885	0	0	0	0	0	0	0	0	0	0	0	0;
	15	1000	0   9999	-9999	1       100	1	1100	0	0	0	0	0	0	0	0	0	0	0	0;
	16	4000	0    990	-990	1       100	1	4100	0	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
	1	54	0	0.0181	0	0	0	0	0	0	1	-360	360;
	2	58	0	0.025	0	0	0	0	0	0	1	-360	360;
	3	62	0	0.02	0	0	0	0	0	0	1	-360	360;
	4	19	0.0007	0.0142	0	0	0	0	0	0	1	-360	360;
	5	20	0.0009	0.018	0	0	0	0	0	0	1	-360	360;
	6	22	0	0.0143	0	0	0	0	0	0	1	-360	360;
	7	23	0.0005	0.0272	0	0	0	0	0	0	1	-360	360;
	8	25	0.0006	0.0232	0	0	0	0	0	0	1	-360	360;
	9	29	0.0008	0.0156	0	0	0	0	0	0	1	-360	360;
	10	31	0	0.026	0	0	0	0	0	0	1	-360	360;
	11	32	0	0.013	0	0	0	0	0	0	1	-360	360;
	12	36	0	0.0075	0	0	0	0	0	0	1	-360	360;
	13	17	0	0.0033	0	0	0	0	0	0	1	-360	360;
	14	41	0	0.0015	0	0	0	0	0	0	1	-360	360;
	15	42	0	0.0015	0	0	0	0	0	0	1	-360	360;
	16	18	0	0.003	0	0	0	0	0	0	1	-360	360;
	17	36	0.0005	0.0045	0.32	0	0	0	0	0	1	-360	360;
	18	49	0.0076	0.1141	1.16	0	0	0	0	0	1	-360	360;
	18	50	0.0012	0.0288	2.06	0	0	0	0	0	1	-360	360;
	19	68	0.0016	0.0195	0.304	0	0	0	0	0	1	-360	360;
	20	19	0.0007	0.0138	0	0	0	0	0	0	1	-360	360;
	21	68	0.0008	0.0135	0.2548	0	0	0	0	0	1	-360	360;
	22	21	0.0008	0.014	0.2565	0	0	0	0	0	1	-360	360;
	23	22	0.0006	0.0096	0.1846	0	0	0	0	0	1	-360	360;
	24	23	0.0022	0.035	0.361	0	0	0	0	0	1	-360	360;
	24	68	0.0003	0.0059	0.068	0	0	0	0	0	1	-360	360;
	25	54	0.007	0.0086	0.146	0	0	0	0	0	1	-360	360;
	26	25	0.0032	0.0323	0.531	0	0	0	0	0	1	-360	360;
	27	37	0.0013	0.0173	0.3216	0	0	0	0	0	1	-360	360;
	27	26	0.0014	0.0147	0.2396	0	0	0	0	0	1	-360	360;
	28	26	0.0043	0.0474	0.7802	0	0	0	0	0	1	-360	360;
	29	26	0.0057	0.0625	1.029	0	0	0	0	0	1	-360	360;
	29	28	0.0014	0.0151	0.249	0	0	0	0	0	1	-360	360;
	30	53	0.0008	0.0074	0.48	0	0	0	0	0	1	-360	360;
	30	61	0.00095	0.00915	0.58	0	0	0	0	0	1	-360	360;
	31	30	0.0013	0.0187	0.333	0	0	0	0	0	1	-360	360;
	31	53	0.0016	0.0163	0.25	0	0	0	0	0	1	-360	360;
	32	30	0.0024	0.0288	0.488	0	0	0	0	0	1	-360	360;
	33	32	0.0008	0.0099	0.168	0	0	0	0	0	1	-360	360;
	34	33	0.0011	0.0157	0.202	0	0	0	0	0	1	-360	360;
	34	35	0.0001	0.0074	0	0	0	0	0	0	1	-360	360;
	36	34	0.0033	0.0111	1.45	0	0	0	0	0	1	-360	360;
	36	61	0.0011	0.0098	0.68	0	0	0	0	0	1	-360	360;
	37	68	0.0007	0.0089	0.1342	0	0	0	0	0	1	-360	360;
	38	31	0.0011	0.0147	0.247	0	0	0	0	0	1	-360	360;
	38	33	0.0036	0.0444	0.693	0	0	0	0	0	1	-360	360;
	40	41	0.006	0.084	3.15	0	0	0	0	0	1	-360	360;
	40	48	0.002	0.022	1.28	0	0	0	0	0	1	-360	360;
	41	42	0.004	0.06	2.25	0	0	0	0	0	1	-360	360;
	42	18	0.004	0.06	2.25	0	0	0	0	0	1	-360	360;
	43	17	0.0005	0.0276	0	0	0	0	0	0	1	-360	360;
	44	39	0	0.0411	0	0	0	0	0	0	1	-360	360;
	44	43	0.0001	0.0011	0	0	0	0	0	0	1	-360	360;
	45	35	0.0007	0.0175	1.39	0	0	0	0	0	1	-360	360;
	45	39	0	0.0839	0	0	0	0	0	0	1	-360	360;
	45	44	0.0025	0.073	0	0	0	0	0	0	1	-360	360;
	46	38	0.0022	0.0284	0.43	0	0	0	0	0	1	-360	360;
	47	53	0.0013	0.0188	1.31	0	0	0	0	0	1	-360	360;
	48	47	0.00125	0.0134	0.8	0	0	0	0	0	1	-360	360;
	49	46	0.0018	0.0274	0.27	0	0	0	0	0	1	-360	360;
	51	45	0.0004	0.0105	0.72	0	0	0	0	0	1	-360	360;
	51	50	0.0009	0.0221	1.62	0	0	0	0	0	1	-360	360;
	52	37	0.0007	0.0082	0.1319	0	0	0	0	0	1	-360	360;
	52	55	0.0011	0.0133	0.2138	0	0	0	0	0	1	-360	360;
	54	53	0.0035	0.0411	0.6987	0	0	0	0	0	1	-360	360;
	55	54	0.0013	0.0151	0.2572	0	0	0	0	0	1	-360	360;
	56	55	0.0013	0.0213	0.2214	0	0	0	0	0	1	-360	360;
	57	56	0.0008	0.0128	0.1342	0	0	0	0	0	1	-360	360;
	58	57	0.0002	0.0026	0.0434	0	0	0	0	0	1	-360	360;
	59	58	0.0006	0.0092	0.113	0	0	0	0	0	1	-360	360;
	60	57	0.0008	0.0112	0.1476	0	0	0	0	0	1	-360	360;
	60	59	0.0004	0.0046	0.078	0	0	0	0	0	1	-360	360;
	61	60	0.0023	0.0363	0.3804	0	0	0	0	0	1	-360	360;
	63	58	0.0007	0.0082	0.1389	0	0	0	0	0	1	-360	360;
	63	62	0.0004	0.0043	0.0729	0	0	0	0	0	1	-360	360;
	63	64	0.0016	0.0435	0	0	0	0	0	0	1	-360	360;
	65	62	0.0004	0.0043	0.0729	0	0	0	0	0	1	-360	360;
	65	64	0.0016	0.0435	0	0	0	0	0	0	1	-360	360;
	66	56	0.0008	0.0129	0.1382	0	0	0	0	0	1	-360	360;
	66	65	0.0009	0.0101	0.1723	0	0	0	0	0	1	-360	360;
	67	66	0.0018	0.0217	0.366	0	0	0	0	0	1	-360	360;
	68	67	0.0009	0.0094	0.171	0	0	0	0	0	1	-360	360;
	27	53	0.032	0.32	0.41	0	0	0	0	0	1	-360	360;
];

%%-----  OPF Data  -----%%
%% generator cost data
%	1	startup	shutdown	n	x1	y1	...	xn	yn
%	2	startup	shutdown	n	c(n-1)	...	c0
mpc.gencost = [
	2	0	0	3	0.04	20	0;
	2	0	0	3	0.0183486239	20	0;
	2	0	0	3	0.0153846154	20	0;
	2	0	0	3	0.0158227848	20	0;
	2	0	0	3	0.0198019802	20	0;
	2	0	0	3	0.0142857143	20	0;
	2	0	0	3	0.0178571429	20	0;
	2	0	0	3	0.0185185185	20	0;
	2	0	0	3	0.0125	20	0;
	2	0	0	3	0.02	20	0;
	2	0	0	3	0.01	20	0;
	2	0	0	3	0.00740740741	20	0;
	2	0	0	3	0.00278473963	20	0;
	2	0	0	3	0.0056022409	20	0;
	2	0	0	3	0.01	20	0;
	2	0	0	3	0.0025	20	0;
];

%% bus names
mpc.bus_name = {
	'1';
	'2';
	'3';
	'4';
	'5';
	'6';
	'7';
	'8';
	'9';
	'10';
	'11';
	'12';
	'13';
	'14';
	'15';
	'16';
	'17';
	'18';
	'19';
	'20';
	'21';
	'22';
	'23';
	'24';
	'25';
	'26';
	'27';
	'28';
	'29';
	'30';
	'31';
	'32';
	'33';
	'34';
	'35';
	'36';
	'37';
	'38';
	'39';
	'40';
	'41';
	'42';
	'43';
	'44';
	'45';
	'46';
	'47';
	'48';
	'49';
	'50';
	'51';
	'52';
	'53';
	'54';
	'55';
	'56';
	'57';
	'58';
	'59';
	'60';
	'61';
	'62';
	'63';
	'64';
	'65';
	'66';
	'67';
	'68';
};
