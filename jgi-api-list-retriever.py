import requests
import json
import os
import csv
import time

# -------------------------
# Configuration
# -------------------------
BASE_URL = "https://files.jgi.doe.gov/mycocosm_file_list/"
# The following organism IDs are obtain by following the instructions from mycocosm_organism_list.xlsm
ORGANISM_IDS = ["Dicsqu464_2","Aaoar1","Abobie1","Chlpad1","Absrep1","Acain1","Acastr1","Acema1","Achma1","Achstr1","Aciri1_iso","Aciri1_meta","Acrchr1","Acrst1","MoamBC1065_1","MoamBC1291_1","MowoN66265_1","Agabi_varbisH97_2","Agabi_varbur_1","Agrped1","Allma1","Altalt1","Altal1","Altbr1","Altro1","Amamu1","Amarub1","Amath1","Ambph1","Amnli1","Amore1","Ampqui1","AmpWSBS2006_1","Amyenc1","Amylap1_1","Amyrou1","Amycha1","Anasp1","Annbov1","Annmae1","Annmin1","Annmor1","Annnit1","Annsty1","Anntru1","Antlo1","Antser1","Apibac1","Apiver1","Aplpr1","Apope1","Armbor1","Armcep1","Armfum1","Armga1","Armlut1","Armme1_1","Armmel1","Armnab1","Armnov1","Armosto1","Armost1","Armtab1","Artol1","Artbe1","Artele1122_1","Clapy1","Ascim1","Ascra1","Ascsa1","Ascni1","Ascru1","Ascap1","Aspacri1","Aspacu1","Aspac1","Aspala1","Aspalbe1","Aspall1","Aspalli1","Aspamb1","Aspamy1","Aspara19utr","Aspaura1","Aspaur1","Aspave1","Aspber1","Aspbom1","Aspbr1","Aspbru1","Aspcae1","Aspcal1","Aspcalif1","Aspcam1","Aspcand1","Aspcar1","Aspcl1","Aspcor1","Aspcos1","Aspcri1","Aspcru1","Aspdese1","Aspegy1","Aspell1","Aspeuc1","Aspfalc1","Aspfij1","Aspfili1","Aspfl1","Aspfl2_3","Aspflo1","Aspfove1","Aspfru1","Aspfu_A1163_1","Aspfu1","Aspger1","Aspgl1","Aspgra1","Asphet1","Asphethal1","Asphom1","Aspibe1","Aspind2_1","Aspind1","Aspins1","Aspjap1","Aspkar1","Aspka1_1","Aspkev1","Asplep1","Aspfo1","Aspluc1","Aspmic1","Aspmin1","Aspmul1_1","Aspnav1_1","Aspne1","Aspneoi1","Aspneo1","Aspnid1","Asplac1","Aspph1","Aspni7","Aspni_DSM_1","Aspni_NRRL3_1","Aspni_bvT_1","Aspnom1","Aspnom13137_1","Aspnov1","Aspnovo1","Aspoch1","Aspoch1432_1","Aspoli1_1","Aspor1","Asppar1","Asppari1","Asppip1","Asppsec1","Asppdef1","Asppsen1","Asppset1","Asppseute1","Asppust1","Aspquaf1","Aspquag1","Aspram1","Asprec1_1","Aspsac1","Aspscle1","Aspscl1","Aspser1","Aspsim1_1","Aspstel1_1","Aspstec1_1","Aspste1","Aspsy1","Asptaic1","Asptam1","Aspte1","Asptetr1","Asptra1","Asptu1","Aspuda1","Aspund1_1","Aspung1","Aspuva1","Aspvad1","Aspvar1","Aspven1","Aspve1","Aspvio1","Aspwel1","Aspwe1","Aspzo1","Astsub1","Aulhe2","Aurpu1","AurpulNBB1","Aurpu_var_mel1","Aurpu_var_nam1","Aurpu_var_pul1","Aurpu_var_sub1","Aurde3_1","Auramp1","Aurvu1","Babin1","Bacci1","Basme2finSC","Batsa1","Bauco1","Beaba1","Corbr1","Benpoi1","Bifad1","Bimnz1","Bisma1","Bisme1","Bismed1","Biscog1","Bjead1_1","Blatri1","Arxad1","Blara1","Blabri1","Blader1","Blade1","Blape1","Blugr2","BlugrR1_1","Blugra3_16","Blyhe1","Boeex1","Boled5","Boledp1","Bolret1","Bombom1","Botbo1","Botdo1_1","Bcine1","Botcin1","Brefa1","Butyri1","Byssp1","Bysci1","CadmalM34_1","Cadsp1","CadmalM221_1","Caecom1","Calth1","Calco1","Calvi1","Calmar1","CtCBS203_1","Thiar1","Canalb1","Canar1","Canbo1","Candu1","Canmem1","Canor1","Canpa1","Canta1","Cante1","Cantro1","Cananz1","Capcor1","Capep1","Capse1","Catan2","Caupr_SCcomb","Caupr1","Cenge3","Cerbo1","Cersp1","CerAGI","Cercau1","Cernew1","Cersam1","Cersc1","Cerbe1","Cerzm1","Cersu1","Chafi1","Chale1","Chafun1","Chafu1","Chagl_1","Chaol1","Chame1","Chagl1","Chathe1","Chalo1","Chivir1","Chocucu1","Chove1","Chylag1","Chyhya1","Chytri1","Cirumb1","Citma1","Clapol1_1","Clarep1_1","Clagr3","Claba1","Claca1","Claim1","Claps1","Claye1","Clasam1","Clasp259_1","Clasp332_1","Clafu1","Clasph1","Clael1","Claaq1","Clapu1","Clalu1_2","Cligib1","Cloaq1","Cloros1","Cocim1","Cocpo1_1","Cocpos1","Cocca1","CocheC4_6","CocheC5_4m","ChetHAW225_4","ChetHm338_1","ChetHm540_1","ChetPR1x412_2","ChetPR9b_4","Coclu2","Cocmi1","Cocsa1","Cocvi1","Cocvi2","Coemoj1","Coere1","Coespi1","Cokrec1","Colab1","Colac2","Colacu1","Colae1","Colca1","Colce1","Colch1","Colchr1","Colco1","Colcu1","Colde1","Coler1","Colfa1","Colsp1","Colfi1","Colfr1","Colfru1","Colgl1","Colgo1","Colgr2","Colhig2","Colin1","Colli1","Collu1","Collup1","Colme1","Colna1","Colny1","Colorb1","Color1","Colpa1","Colph1","Colpl1","Colsa1","Colsia1","Colsi1","Colsoj1","Colso1","Colsu1","Colsub1","Colta1","Colto1","Coltof1","Coltro1","Coltr1","Colzo1","Conco1","Conth1","Conlig1","ColoR110_1","Conioc1","Conol1","Conpu1","Conap1","Copang1","Copmic2","Copci1","Copci_AmutBmut1","Copcin2","Copmar1","Copph3","CopCBS38678_1","Cormi1","CorRAO_2017_1","Corin1","Corno1","Corse1","Corca1","Crafun1","Crevar1","Croqu1","Crula1","Cryan3","Crymi1","Crypa2","Cryam1","Crycu1","CgaCA1873_1","CgaVGII_1","CgaVGIV_1","CgaWM276_1","Cryne_JEC21_1","Cryne_H99_1","Cryte1","Tsuwi1","Cucbe1","Cunech1","Cyapal1","Cyaste1","Cyastr2","Cybfa1","Cybja1","Cylto1","Cylol1","Cypeu1","Rhomi1","Cytmel1","Dacsp1","Daces1","Dacma1","Daequ1","Dalba1","Dalcal1","Daldec1","DalEC12_1","Dales1","Dalgra1","DallocAZ0526_2","Dalloc1","DaFL1419_1","Dalver1","Debfa1","Debfab1","Debha1","Decga1","Dekbr2","Delco1","Delst1","Denbi1","Denna1","Densp1","Diaam1","Diahe1","Dibbae1","Dicsqu463_1","Dicsqu464_1","Dicsq1","Dicsqu18370_1","Dicele1","Didex1","Didma1","DimcrSC1","Diohu1","Dipse1","Dipgro1","Diptot1","Dipuni1","Disac1","Disorn1","DiorN22417_1","Dotsy1","Dotse1","Dreco1","Drest1","Durrog2","Earsca1","Echmac1","Edhae1","Elagr1","Elsamp1","Emepa1","AcreTS7_1","Emmcr1","Emmpa1","Enccu1","Enche1","Encin1","Encro1","Endpal1","EndpusZ1","Endsp1","Entbi1","Enthe1","Entca1","MobeAD1040_1","MochAD033_1","MochN2769_1","HaliN2525_1","Enthel1","Epityp1","Erebi1","Erecy1","Ashgo1_1","Erego1","Erynec1","Erypu1","Escweb1","Eurhe1","Eutla1","Exigl1","Exoaq1","Exode1","Exome1","Exool1","Exosi1","Exosp1","EurotioJF033F_1","EurotioJF034F_1","Exoxe1","Favcal1_2","Fenlin1","Fibra1","Fibsp1","Filflo1","Fimjon1","Fishe1","Fomfom1","Fomme1","Pipbet1_1","Fompi3","Foner1","Fonmo1","Fonmu1","Fonnu1","Fonpe1","Frien1","Frisi1","Fustri1","Fusco1","Fuscu1","Fusfu1","Fusgr1","Fusla1","Fusma1","FusoxFo47","FusoxFo47_2","FoxFo5176","Fusoxys1","Fusoxy1","Fusox32931","Fusoxalb1","Fusoxcon1","Fusoxcub1","Fusox2","Fusoxlyc1","Fusoxmel1","Fusoxpis1","Fusoxrad1","Fusoxrap1","Fusoxvas1","FoxII5","Fuspo1","Fuspro1","Fuspr1","Fusps1","Fusre1","Fusso1","Fuseq1","Fustr1","Necha2","Fusven1","Fusve2","Gaesem1","Gaegr1","Galma1","MomuN6456_1","Ganbon1","Ganleu1","Ganluc1","Gansi1","Gansp1","Gaumor1_1","Geocar1","Geopyr1","Gervar1","Gigmar1","Gigro1","Gilper1","Glalo1","Glopol1","Glocon1","Glotr1_1","Glost2","GciUMSG1_1","GciUMSG3_1","Ganpr1","Gonbut1","Gorhay1","Grascr1","Grocl1","Mocy1230_1","Guyne1","Gymjun1","Gyman1","Gymlu1","Gyrli1","Gyresc1","Gyrinf1","Halrad1","Hangu1","Hanop1","Hanos1","Hanuv1","Hanva1_1","HabiNA12553_1","HaspN3175_1","HapNA10739_1","HapNA10996_1","Hebcy2","Helgr1","Helpul1","Helsul1","Heper1","Hesve2finisherSC","Hetan2","Hexnit1","Hirmi1","Hisca1","Hompol1","Horac1","Horth1","Horwer1","Humhy1","Hyacur1","Hydpi2","Hydfim1","Hydru2","Hygaur1","Hymrad1","Hypsu1","Hypbu1","Hypper1","Hypros1","Hyparg1","Hypcer1","Hypcro1","Hypfra2","Hypfus1","Hypmon1","Hyprub1","HyprubER1909_1","HypCI4A_1","HypCO275_1","HypEC38_3","HyFL0543_1","HyFL0890_1","HyFL1150_1","HyFL1284_2","HyFL1857_1","HyNC0597_1","HyNC1633_2","Hypsub2","Hyptru1","Hypma1","Hyssto1","Hyspu1_1","Ilysp1","Ilyeu1","Neora1","Irplac1","Corfu1","Jaaar1","Jamsp1","Jimfl_AD_1","Jimfl_GMNB39_1","Jimlac1","Kalpfe1","Kalbr1","Karrh1","Kazaf1","Kazna1","Kicala1","Klula1","Kluma1","Kocim1","KdCBS826_1","Kredeu1","Krezon1","Kurca1","Lacam2","Lacbi2","Lacda1","Lacfe1","Lacla1","Lacme1","Lacmi1","Lacno1","Lacqu1","LacCBS6924_1","Lacth1","Lacaka1","Lacdel1","Lachat1","Lachen1","Lacind1","Lacpsa1","Lacpse1","Lacqui1","Lacsan1","Lacviv1","Lacsub1","Lacvol1","Laesu1","Lanmao1","Lasmin1","Lasov1","Lashir1","Lashi1","Corco1","Tralac1","Tramen1","Leisp1","LacJLM2183_1","Lbo_TFB10291_1","LboTFB10292_1","LlaTMI1499_1","Lenafn_TMI1502_1","Lbo_TFB10827_1","LboTFB7810_1","LboTFB7829_1","LedB17_3","Led_CS584_1","Lenedo1","Lened1","LedTMI1148_1","LedTMI1633_1","LedVB361_1","Lentinedodes1","Lenafn1","LboET3784_1","Lenlat1","LlaRV95_379_1","LnoICMP18003A_1","Lennov1","Lenrap1","LraINPA1820_1","LraJLM1587_1","Lenra_T_1","LraTFB9207_1","Lenrap1_155","Lenti6_1","Lenti7_1","Lenfl1","Phimu1","ColoR113_1","Leppa1","Lepnud1","Lepor2","Lepmu1","Leugo1_1","Leumo1","Leucr1","Liccor1","Lichy1","Licra1","Linpe1","Linin1","Linrh1","MocaN2610_1","MoelGBA34_1","MoelGBA40_1","MoelNVP5_1","MoelNVP71_1","MoexN28262_1","MogaAD045_1","MogaNVP60_1","MoscN6426_1","MozyN2592_1","MozyPUSTF9C_1","Liparx1","Lipchi1","Ldo8726_1","Lipodoor1","Lipdoo1","Lipjap1","Lipokono1","Lipkon1","Lipmes1","Lipoli1","Lipori1_1","Lipsmi1","Lst7536_1","Lst7851_1","Lst8064_1","Lipst1_1","Lipstark1_1","Lipstar1_1","Lipsta1_1","Lipsuo1","Liptetr1","Liptet1","Liptetra1","Lipotetr1","Lizem1","Lobtra1","EctrN5525_1","Lodelo1","Lompr1","Lopma1","Lopnu1","Lopmy1","Lyoat1","Macfu1","Macpha1","Macph1","Macan1","Madmy1","Magpo1","Malgl1","Malpa1","Malsy1_1","Malve1","Malci1","Marfi1","Marbr1","Marpt1","Maseb1","Masph1","Meimi1","Melame1","Mellp2_3","Melli1","Melli2_C","Melli2_H","Melbro1","Melpu1","Melbi2","Melva1","Metac1","Metal1","Metani1","Metbr1","Metgui1","Metma1","Metri1","Metro1","Metbi1","Metbi_SCcomb","Metfru2","Meygui1","Theste1","Micin1","Micld1","Micbo1","Mictri1","Micca1","Micmi1","Mitdap1","Mixos1","MoreMES2147_1","Moeli1","Moean1","Moeaph1","Monha1","Monpe1_1","MroMCA2997_1","Morco1","Morimp1","Morsny1","MoalAD071_1","MoalAD072_1","MoalCK1249_1","MoalGBA31_1","MoalN66262_1","MoanKOD1229_1","MoclN2760_1","Morel2","Morel_U14_1","MoeNVP64_1","MoglAD054_1","MoglREB010B_1","Morhum1","MohyN2591_1","Mormul1","MopoKOD948_1","Mosp14UC_1","MospAD010_1","MospAD011_1","MospAD031_1","MospAD032_1","MospAD094_1","MospAM989_1","MospGBA30_1","MospGBA35_1","MospGBA39_1","MospGBA43_1","MorGBAus27b_1","MospKOD1030_1","MospNVP41_1","MospNVP85_1","Mucam1","Muccirc1","Mucend1","Mucfus1","Muclan1","Muccir1_3","Mucci3","Mucmuc1","Mucrac1","Muloch1","Mychet1","Myche1","Corsim1","Spoth2","Mycalb1","Mycale1","Mycami1","Mycbel1","Mycrub1","Myccro1","Mycepi1","Mycfil1","Mycflo1","Mycgale1","Mycgal1","Mychae1","Myclat1","Myclep1","Mycmac1","Mycmet1","Mycoli1","Mycpol1","Mycpur1","Mycreb1","Mycros1","Mycsan1","Myc59_1","Mycvit1","Mycvul1","Mycden1","Myceu1","Mycgr3","Mycth1","Mycthe1","Mycafr1","Myrdu1","Mytre1","Myxme1","Nadfu1","Treen1","Nagfr2","Nagvi1","Nakbac1","Nakdel1","Nakwi1","Nangy1","Nauca1","Nauda1","Nemabo1","Nemdif1","NsAK0226_1","NsAZ0576_1","NsCB679_1","NeFL0031_2","NeFL0916_1","Nemani1","Nemdi1","Nempa1","Neosp1","Neolan1","Neopa1","Neoirr1","Neole1","Neodi1","Neofi1","Neucr_trp3_1","Neucr2","Neucr4830_1","Neuhi1","Neuin1","Neute_matA2","Neute_mat_a1","Gelte1","Nosap1","Nosbo1","Nosce1","Obbri1","Obemuc1","Ocuya1","Ogapa1","Hanpo2","Oidma1","Oidneo1","Olipa1","Olpbor1","Ompol1","Ophdi1","Ophau1","Ophca1","Ophun1","Ophsi1","Ophnu1","OphpiCECT20416_2","Ophpic1","Ordco1","MicG_I_3","Orpsp1_1","Oudmuc1","Pacta1_2","Bysni1","Paevar1","Paevar_HGY_1","Panpap1","Panru1","Papla1","Parbr1","Parbra1","Parlu1","Parsp1","Paroc1","Parsa1","Parch1","Parchr1","Parsed1","Parpar1","Thiap1","Thihy1","Parpo1","Patat1","Paxru2","Paxam1","Paxin1","Pecora1","Penant1","Penar1","Pcas15300_1","Penbra1","Pbre18316_1","Pencam1","PenchWisc1_1","Pench1","Pencop1","Pcvj18317_1","Pendec1","Pendi1","Pendig1","Penexp1","Penfla1","Penfr1","Pengri1","Penita1","Pennal1","Pennord1","Penoc1","Penox1","Penpol1","Penro1","Pensol1","Psol18327_1","Penste1","Pensub1","Penth1","Penvul1","Ricme1","Perma1","Pesfi1","Pestal1","Petxy1","Pezech1","Phaal1","Phach1","Phapo1","PhapaK8108","Phapa1","PpacPPUFV02","Phaca1","Phchr2","Phaart1","Pheno1","Pheni1","Phiatr1","Acrth1","Phisc1","Phisu1","Phiatt1","Phlbr1","Phlcen1","Phlrad1","Phlgi1","PhlFC14_2","Corgl3","Phoaln1","Phocon1","Phohig1","Photr1","Phybl_L51_1","Phybl2","PhyblU21_2","PnitS608_1","Phcapit2","Phcap1","Pcapi1","Phycap1","Phycapi2","Phcapi1","Pcitr2","Phycit1","Pcitri2","Phcit1","Pcit17464","Pcit120373","Pcit11120","Pcit122482","Pcit122670","Phycitr1","Pcit131864","Pcit141352","Pcit16586","Pcit129764","Phcitr1","Phy27169","Phypa1","Phycpc1","Pickud1","Picme2","Picpa1","Pieho1_1","Pilano1","Pilumb1","Pilcr1","Pincor1_1","Pipcy3_1","Piptie1","Pirin1","Pirfi3","PirE2_1","Pisalb1","Pisthe227_1","Piscro1","Pismar1","Pismi2","Pisori2","Pismi_AB1_1","Pisthe1","Pisti2","Plecuc1","Plesi1","Pleery1","PleosPC15_2","PleosPC9_1","Plicr1","Plucer1","Pneca1","Pneji1","Pnejir1","Pnemu1","Pocchl1","MoclAM1000_1","MoclKOD947_1","MoepAD058_1","MoepKOD1059_1","MoepN5512_1","MohoAD009_1","MohoCK413_1","MohuKOD1050_1","MomiAD069_1","MomiNVP1_1","MoveAD079_1","MoveN2611_1","MoveTTC192_1","Podcom1","Podan3","Podap1","Podaus1","Poddec1","Poddi1","Podfim1","Podbra1","Podtet1","Polci1","Polagg1_1","Polfu1","Polar1","Polbr1","Polsqu1","Polhy1","Porpun1","Porspa1","Pospl1","PosplRSB12_1","Powhir1","Prola1","Mycfi2","Psemus1","Pseudest1","Pse03VT05_1","PseVKM103_1","PseVKM3775_1","PseVKM4246_1","PseVKM4514_1","PseVKM4520_1","Psever1","Pseneu1","Pseve2","Rhodsp1","Gelamo1","Psehy1","Psean1_1","Psefl1","Psehu1","Psicub1_1","Psiser1","Ptegra1","PuccoNC29_1","PuccoSD80_1","Pgt_201_A1","Pgt_201_B1","Pgt_Ug99_A1","Pgt_Ug99_C1","Pucgr2","Pucstr1","Pucst1","Pucst_PST78_1","Puctr1","Punst1","Purli1","Pycci1","Pycco1","Pycpun1","Pycsa1","Pyrly1","Pyrsp1","Pyrtt1","Pyrtr1","Magor1","Pyrco1","Pyrdom1","Pyrom1","Racan1","Rac5018_1","Radspe1","Ramac1","Rambr1","Rasby1","Talem1","Remth1","Rhesp1","Rhima1","Rhihy1","Rhiso1","Rhisol1","Rhisola1","Rhili1","Rhipu1","Rhice1_1","Rhicl1","Rhidi1","Rhiir4401_1","RhiirA1_2","RhiirA4","RhiirA5","RhiirB3_2","RhiirC2_2","Gloin1","RhiirDAOM197198_2","Rhives1","Rhivi1","Rhior3","Rhimi59_2","Rhich1","Rhimi1_1","Rhimi_ATCC52814_1","Rhier1","Rhobut1_1","Fomros1","Rhoglu91_1","Rhoto_IFO0559_1","Rhoto_IFO0880_4","Rhoto_IFO1236_1","Rhoto1","Rhoba1_1","RhoCCFEE5036_1","Rhosp1","Rhota1","Rhyag1","Rhyco1","Rhyse1","Rhyru1_1","Ricfib1","Ricmel1","Rigmic1","Rorror1","Rosne1","Roster1","Rozal1_1","Rozal_SC1","Rusbre1","Ruscom1","Rusdis1","Rusear1","Ruseme1","Rusoch1","Rusrug1","Rusvin1","Sacpr1","Sacarb1","Sacboulardii_1","Sacce_GLBRCY223_1","SacceM3707_1","SacceM3836_1","SacceM3837_1","SacceM3838_1","SacceM3839_1","Sacce1","Saceu1","SacAshbya_1","Sacca1","Saico1","Sakvas1","Satdi1","Sceap1","Schama1","Schcoi1","Picst3","Schxyl1","Schco2071_1","Schco2231_1","Schco2251_1","Schco2271_1","Schco2272_1","Schco3","Schco_LoeD_1","Schco_TatD_1","SchcoZB1","SchcoZB2","Schfas1","Schpa1","Schcy1","Schja1","Schoc1","Schpo1","Schcon1","Schves1","Sclci1","Sclcihr1","Sclyun1","Sclbo1","Sclsc1","Sebve1","Sepmu1","Seppo1","Serla_varsha1","SerlaS7_3_2","SerlaS7_9_2","Setho1","Settu3","ClaPMI390","Sisni1","Sissu1","SmicuMNP_2","SmiculW2_1","Smimuc2","Acral2","Sodal1","Sorbr1","Sorhu1","Sorma1","Spapa3","Sphst1","Sphbr2","Spifus1","Spipu1","Spore1","Spoumb1","Spofi1","Spobr1","Spoin1","Sposc1","Sprlo1","Stach1","Stachl1","Stael1","Stano2","Stasp1","Stalo1","Stasorb1","Stely1","Stehi1","Suiame1","Suiamp1","Suibov1","Suibr2","Suisubl1","Suicli1","Suicot1","Suidec1","Suidis1","Suifus1","Suihi1","Suilak1","Suilu4","Suiocc1","Suipal1","Suipla1","Suiplo1","Suipic1","Suisu1","Suisub1","Suitom1","Suivar1","Suigr1","Synrac1","Synfus1","Synplu1","Synps1","Talat1","Talabor1","Talis1","Talma1_2","Talst1_2","Tapde1_1","Ternu1","Terbo2","Tercla1","TerJ132_1","Tescy1","Tetbla1","Tetpha1","Thaele1","Thasp1","Thacu1","Thega1","Theter1","Theau2","Thecr1","Theth1","Thiau1","Talth1","Thela1","Thelan1","Thefe1","Thehi1","Themy1","Thite2","Thipu1","Tilcar1","Tilco1","Tilin1","Tilwal1","Tilan2","Tilwa1","Tirniv1","Tolca1","Tolinf1","Tolop1","Tolpa1","Torhe1","Canca1","Torde1","Totfu1","Traho1","Trabet1","Traci1","Tragib1","Tralj1","Tramax1","Tramey1","Trapol1","Trapub1","Traver1","Trave1","Trace1","Trepe1","Treme1","Tripra1","Thian1","Humgr1","Tribi1","Triaru1","Triasper1","Triasp1","Trias1","Triatrob1","Triat2","Tribre1","Trici4","Trigam1","Trigui1","Triham1","Triha1","Trihar1","Trilo3","Tripar1","Triple1","TrireMAT11_1","TrireMAT12_1","Trire_Chr","TrireRUTC30_1","Trire2","TrispAM6_1","TriviGv29_8_2","Trima3","Trihyb1","Trieq1","Triin1","Trime1","Triru1","Triso1","Trito1","Triver1","Trivi1","Trias2479","Trias8904","Triol1","Triarc1","Truan1","Tubae1","Tubbor1","Tubbr1_1","Tubin1_1","Tubma1","Tubme1v2","Tulca1","Umbra1","Umbsp_AD052_1","Umbpus1","Uncre1","Ustvir1","Ustbr1","Usthor1","Ustma2_2","Valma1","Vanpo1","Varmin1","Vavcu1","Veneff1","Venin1","Venpi1","Verga1","Veren1","Veral1","Verdah1","Verda1","Verlo1","Ustsp1","Tryvi1","Vitco1","Volvo1","Walic1","Walse1","Wesor1","Whamic1","Wicso1","Wican1","Wilmi1","Wolco1","Xerba1","Xylacu1","Xylarb124340_1","XylarbFL1030","Xylbam139988_1","Xylcas124033_1","Xylhel2","Xylcube1","Xylcur114988_1","Xyldig1","Xylcub1","Xylgra1","Xylint1","Xyllon1","Xylni1","Xylpal124036_1","Xylscr1","Xy124048_1","XylFL0043","XyFL0064_1","XylFL0933","XylFL1042","XyFL1777_1","Xyltel121673_1","Xylven1","XyAK1471_1","XylFL0016","XylFL0255","XylFL0594","XylFL0662B","XyFL0804_2","XylFL1019","XyFL1272_2","XylFL1651","Plecto1","XyFL0641_1","XylFL2044","Xylhe1","Yarli1","YarliW29_1","Yarlip1","YarliY64008_1","YarliW29","YarliYB392","YarliYB419","YarliYB420","YarliYB566","YarliYB567","YarliYlCW001","Zalva1","Zancul2","Zasce1","Zoorad1","Zoprh1","Zycmex1","Zygro1","Zygrou1","Zymar1","Zymbr1","Zymps1","Zymtr1"]  # Add your list of organism IDs here
FILES_PER_PAGE = 50  # Set to 50 files per page
REQUEST_DELAY = 1  # Delay in seconds between requests
JSON_FOLDER = "json_files"  # Folder for all JSON files

# Authentication headers
headers = {
    "accept": "application/json",
    "Authorization": "test"  # Replace with your token or os.getenv("JGI_TOKEN")
}

# -------------------------
# Fetch and save JSON file list for each organism
# -------------------------
def fetch_all_files(organism_id):
    print(f"Fetching all files for {organism_id} from JGI...")
    params = {
        "organism": organism_id,
        "api_version": 2,
        "a": "false",  # Exclude archived
        "h": "false",  # Exclude hidden
        "d": "asc",    # Sort ascending
        "p": 1,        # Page number (start at 1)
        "x": FILES_PER_PAGE,  # Files per page
        "t": "simple"
    }

    # Create the JSON folder if it doesn't exist
    os.makedirs(JSON_FOLDER, exist_ok=True)

    page = 1
    total_files = 0

    try:
        while True:
            params["p"] = page  # Update page number
            print(f"Fetching page {page} for {organism_id}...")
            response = requests.get(BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Get files from the current page
            current_files = data.get("organisms", [{}])[0].get("files", [])
            if not current_files:  # Break if no files are returned
                print(f"No more files found for {organism_id}. Stopping pagination.")
                break

            total_files += len(current_files)
            print(f"Found {len(current_files)} files on page {page} for {organism_id}.")

            # Save current page to a JSON file in the JSON folder
            page_filename = os.path.join(JSON_FOLDER, f"all_files_{organism_id}_page_{page}.json")
            with open(page_filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Saved page {page} to {page_filename}")

            page += 1
            time.sleep(REQUEST_DELAY)  # Delay between requests

        if total_files == 0:
            print(f"❌ No files found for {organism_id} across any pages.")
        else:
            print(f"✅ Total {total_files} files saved for {organism_id}.")
        return total_files > 0

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {organism_id}: {e} - {response.status_code}: {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request error for {organism_id}: {e}")
        return False
    except Exception as e:
        print(f"General error for {organism_id}: {e}")
        return False

# -------------------------
# Parse and filter JSON files locally, then export to CSV
# -------------------------
def parse_and_export():
    found = []
    # Ensure the JSON folder exists
    if not os.path.exists(JSON_FOLDER):
        print(f"No {JSON_FOLDER} folder found. Please run fetch_all_files() first.")
        return

    for organism_id in ORGANISM_IDS:
        json_files = [f for f in os.listdir(JSON_FOLDER) if f.startswith(f"all_files_{organism_id}_page_") and f.endswith(".json")]
        if not json_files:
            print(f"No JSON files found for {organism_id} in {JSON_FOLDER}. Skipping.")
            found.append({
                "organism": organism_id,
                "file_name": "NO FILES FOUND",
                "file_id": "",
                "_id": "",
                "file_status": "",
                "md5sum": "",
                "file_date": "",
                "ncbi_taxon_id": "",
                "jat_label": "",
                "ncbi_taxon_class": "",
                "ncbi_taxon_family": "",
                "ncbi_taxon_order": "",
                "ncbi_taxon_genus": "",
                "ncbi_taxon_species": "",
                "file_type": "",
                "portal_display_location": ""
            })
            continue

        print(f"Processing files for {organism_id}...")
        organism_file_count = 0
        
        for json_file in sorted(json_files):  # Sort to process pages in order
            json_file_path = os.path.join(JSON_FOLDER, json_file)
            print(f"Parsing {json_file}...")
            with open(json_file_path, "r") as f:
                data = json.load(f)

            files = data.get("organisms", [{}])[0].get("files", [])
            organism_file_count += len(files)
            print(f"Found {len(files)} files in {json_file}.")

            for file in files:
                metadata = file.get("metadata", {})
                ncbi_taxon = metadata.get("ncbi_taxon", {})
                portal = metadata.get("portal", {})
                
                found.append({
                    "organism": organism_id,
                    "file_name": file.get("file_name"),
                    "file_id": file.get("file_id"),
                    "_id": file.get("_id"),
                    "file_status": file.get("file_status"),
                    "md5sum": file.get("md5sum"),
                    "file_date": file.get("file_date"),
                    "ncbi_taxon_id": metadata.get("ncbi_taxon_id", ""),
                    "jat_label": metadata.get("jat_label", ""),
                    "ncbi_taxon_class": ncbi_taxon.get("ncbi_taxon_class", ""),
                    "ncbi_taxon_family": ncbi_taxon.get("ncbi_taxon_family", ""),
                    "ncbi_taxon_order": ncbi_taxon.get("ncbi_taxon_order", ""),
                    "ncbi_taxon_genus": ncbi_taxon.get("ncbi_taxon_genus", ""),
                    "ncbi_taxon_species": ncbi_taxon.get("ncbi_taxon_species", ""),
                    "file_type": file.get("file_type", ""),
                    "portal_display_location": portal.get("display_location", "")
                })
                    
        # If no match found across all pages
        if organism_file_count == 0:
            print(f"⚠️ No files in parsed pages for {organism_id}.")
            found.append({
                "organism": organism_id,
                "file_name": "NO FILES FOUND",
                "file_id": "",
                "_id": "",
                "file_status": "",
                "md5sum": "",
                "file_date": "",
                "ncbi_taxon_id": "",
                "jat_label": "",
                "ncbi_taxon_class": "",
                "ncbi_taxon_family": "",
                "ncbi_taxon_order": "",
                "ncbi_taxon_genus": "",
                "ncbi_taxon_species": "",
                "file_type": "",
                "portal_display_location": ""
            })

        # Export to CSV
        output_file = "all_files_metadata.csv"
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "organism", "file_name", "file_id", "_id", "file_status", "md5sum",
                "file_date", "ncbi_taxon_id", "jat_label", "ncbi_taxon_class",
                "ncbi_taxon_family", "ncbi_taxon_order", "ncbi_taxon_genus",
                "ncbi_taxon_species", "file_type", "portal_display_location"
            ])
            writer.writeheader()
            writer.writerows(found)
            
        print(f"✅ Exported {len(found)} matching files to proteins_filtered_files.csv")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    for organism_id in ORGANISM_IDS:
        # Check if any JSON files exist for this organism to avoid re-fetching
        if not any(f.startswith(f"all_files_{organism_id}_page_") for f in os.listdir(JSON_FOLDER)):
            fetch_all_files(organism_id)
        else:
            print(f"🗂️ Using cached JSON for {organism_id}...")

    parse_and_export()