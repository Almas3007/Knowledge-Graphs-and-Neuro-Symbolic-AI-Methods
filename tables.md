# KGNS-DR results

Mean ± SD over 5 seeds. Selection used the internal validation split only.


## biomedclip - Internal test (Public-DR-v1)

| Model | Accuracy | Balanced acc. | Macro-F1 | QWK | ECE | Referable AUC | Recall severe |
|---|---|---|---|---|---|---|---|
| ZS-Grade | 0.385 ± 0.000 | 0.326 ± 0.000 | 0.319 ± 0.000 | 0.567 ± 0.000 | 0.077 ± 0.000 | 0.837 ± 0.000 | 0.114 ± 0.000 |
| NN | 0.673 ± 0.005 | 0.518 ± 0.010 | 0.522 ± 0.006 | 0.694 ± 0.001 | 0.034 ± 0.005 | 0.890 ± 0.001 | 0.366 ± 0.060 |
| CBM-KG | 0.630 ± 0.001 | 0.431 ± 0.007 | 0.425 ± 0.010 | 0.631 ± 0.003 | 0.040 ± 0.010 | 0.830 ± 0.002 | 0.295 ± 0.030 |
| KG-Sym-T | 0.621 ± 0.001 | 0.399 ± 0.001 | 0.399 ± 0.002 | 0.585 ± 0.001 | 0.027 ± 0.004 | 0.824 ± 0.000 | 0.191 ± 0.005 |
| KG-Sym | 0.629 ± 0.002 | 0.404 ± 0.004 | 0.401 ± 0.004 | 0.609 ± 0.003 | 0.025 ± 0.003 | 0.833 ± 0.002 | 0.145 ± 0.020 |
| NS-Fuse | 0.674 ± 0.006 | 0.518 ± 0.010 | 0.522 ± 0.006 | 0.696 ± 0.004 | 0.034 ± 0.005 | 0.889 ± 0.001 | 0.366 ± 0.060 |
| NS-Fuse-T | 0.677 ± 0.005 | 0.515 ± 0.010 | 0.521 ± 0.007 | 0.698 ± 0.002 | 0.034 ± 0.005 | 0.889 ± 0.000 | 0.357 ± 0.054 |
| NS-Joint | 0.672 ± 0.004 | 0.511 ± 0.004 | 0.513 ± 0.005 | 0.694 ± 0.003 | 0.034 ± 0.006 | 0.886 ± 0.004 | 0.320 ± 0.015 |

## biomedclip - External: DeepDRiD

| Model | Accuracy | Balanced acc. | Macro-F1 | QWK | ECE | Referable AUC | Recall severe |
|---|---|---|---|---|---|---|---|
| ZS-Grade | 0.192 ± 0.000 | 0.283 ± 0.000 | 0.204 ± 0.000 | 0.356 ± 0.000 | 0.176 ± 0.000 | 0.760 ± 0.000 | 0.100 ± 0.000 |
| NN | 0.334 ± 0.006 | 0.361 ± 0.007 | 0.272 ± 0.003 | 0.384 ± 0.015 | 0.337 ± 0.007 | 0.826 ± 0.003 | 0.138 ± 0.016 |
| CBM-KG | 0.414 ± 0.004 | 0.361 ± 0.005 | 0.295 ± 0.005 | 0.458 ± 0.011 | 0.166 ± 0.006 | 0.792 ± 0.008 | 0.100 ± 0.012 |
| KG-Sym-T | 0.393 ± 0.004 | 0.324 ± 0.003 | 0.265 ± 0.004 | 0.323 ± 0.006 | 0.158 ± 0.002 | 0.751 ± 0.001 | 0.078 ± 0.004 |
| KG-Sym | 0.364 ± 0.001 | 0.328 ± 0.000 | 0.251 ± 0.000 | 0.290 ± 0.011 | 0.182 ± 0.007 | 0.754 ± 0.003 | 0.058 ± 0.002 |
| NS-Fuse | 0.335 ± 0.007 | 0.361 ± 0.007 | 0.272 ± 0.003 | 0.383 ± 0.014 | 0.335 ± 0.010 | 0.826 ± 0.003 | 0.134 ± 0.020 |
| NS-Fuse-T | 0.340 ± 0.005 | 0.363 ± 0.008 | 0.275 ± 0.004 | 0.386 ± 0.014 | 0.328 ± 0.012 | 0.825 ± 0.002 | 0.130 ± 0.018 |
| NS-Joint | 0.344 ± 0.017 | 0.366 ± 0.011 | 0.273 ± 0.015 | 0.405 ± 0.027 | 0.318 ± 0.030 | 0.827 ± 0.005 | 0.108 ± 0.024 |

## flair - Internal test (Public-DR-v1)

| Model | Accuracy | Balanced acc. | Macro-F1 | QWK | ECE | Referable AUC | Recall severe |
|---|---|---|---|---|---|---|---|
| ZS-Grade | 0.724 ± 0.000 | 0.656 ± 0.000 | 0.588 ± 0.000 | 0.826 ± 0.000 | 0.044 ± 0.000 | 0.959 ± 0.000 | 0.739 ± 0.000 |
| NN | 0.806 ± 0.004 | 0.696 ± 0.007 | 0.680 ± 0.006 | 0.863 ± 0.005 | 0.018 ± 0.004 | 0.969 ± 0.001 | 0.593 ± 0.030 |
| CBM-KG | 0.788 ± 0.008 | 0.651 ± 0.008 | 0.644 ± 0.003 | 0.857 ± 0.002 | 0.037 ± 0.006 | 0.960 ± 0.000 | 0.464 ± 0.058 |
| KG-Sym-T | 0.774 ± 0.001 | 0.534 ± 0.002 | 0.506 ± 0.002 | 0.834 ± 0.000 | 0.086 ± 0.001 | 0.952 ± 0.000 | 0.000 ± 0.000 |
| KG-Sym | 0.799 ± 0.001 | 0.626 ± 0.009 | 0.635 ± 0.009 | 0.854 ± 0.003 | 0.033 ± 0.004 | 0.955 ± 0.001 | 0.407 ± 0.050 |
| NS-Fuse | 0.806 ± 0.004 | 0.696 ± 0.007 | 0.680 ± 0.006 | 0.863 ± 0.005 | 0.018 ± 0.004 | 0.969 ± 0.001 | 0.593 ± 0.030 |
| NS-Fuse-T | 0.806 ± 0.004 | 0.696 ± 0.007 | 0.680 ± 0.006 | 0.863 ± 0.005 | 0.018 ± 0.004 | 0.969 ± 0.001 | 0.593 ± 0.030 |
| NS-Joint | 0.807 ± 0.002 | 0.686 ± 0.007 | 0.679 ± 0.003 | 0.860 ± 0.002 | 0.022 ± 0.007 | 0.968 ± 0.001 | 0.539 ± 0.034 |

## flair - External: DeepDRiD

| Model | Accuracy | Balanced acc. | Macro-F1 | QWK | ECE | Referable AUC | Recall severe |
|---|---|---|---|---|---|---|---|
| ZS-Grade | 0.561 ± 0.000 | 0.540 ± 0.000 | 0.504 ± 0.000 | 0.779 ± 0.000 | 0.078 ± 0.000 | 0.953 ± 0.000 | 0.496 ± 0.000 |
| NN | 0.495 ± 0.072 | 0.403 ± 0.022 | 0.367 ± 0.034 | 0.510 ± 0.103 | 0.223 ± 0.058 | 0.849 ± 0.081 | 0.062 ± 0.016 |
| CBM-KG | 0.361 ± 0.148 | 0.385 ± 0.086 | 0.281 ± 0.107 | 0.370 ± 0.298 | 0.258 ± 0.180 | 0.947 ± 0.004 | 0.477 ± 0.076 |
| KG-Sym-T | 0.525 ± 0.001 | 0.441 ± 0.003 | 0.380 ± 0.002 | 0.758 ± 0.001 | 0.060 ± 0.003 | 0.948 ± 0.000 | 0.000 ± 0.000 |
| KG-Sym | 0.067 ± 0.005 | 0.204 ± 0.002 | 0.030 ± 0.005 | 0.012 ± 0.006 | 0.760 ± 0.061 | 0.948 ± 0.003 | 0.000 ± 0.000 |
| NS-Fuse | 0.495 ± 0.072 | 0.403 ± 0.022 | 0.367 ± 0.034 | 0.510 ± 0.103 | 0.223 ± 0.058 | 0.849 ± 0.081 | 0.062 ± 0.016 |
| NS-Fuse-T | 0.495 ± 0.072 | 0.403 ± 0.022 | 0.367 ± 0.034 | 0.510 ± 0.103 | 0.223 ± 0.058 | 0.849 ± 0.081 | 0.062 ± 0.016 |
| NS-Joint | 0.514 ± 0.077 | 0.473 ± 0.050 | 0.391 ± 0.062 | 0.641 ± 0.119 | 0.172 ± 0.060 | 0.912 ± 0.016 | 0.209 ± 0.057 |

## Explanation faithfulness (concept deletion, mean over seeds)

Comprehensiveness = drop in predicted-grade probability when the cited lesions are set absent; random = same number of uncited lesions removed. Flip = predicted grade changes.

| Encoder | Cohort | Model | n explained | Compr. (cited) | Compr. (random) | Flip (cited) | Flip (random) |
|---|---|---|---|---|---|---|---|
| biomedclip | deepdrid | CBM-KG | 772 | -0.219 | 0.290 | 0.231 | 0.813 |
| biomedclip | deepdrid | KG-Sym | 861 | 0.185 | -0.005 | 0.765 | 0.130 |
| biomedclip | deepdrid | KG-Sym-T | 762 | 0.298 | -0.007 | 0.960 | 0.081 |
| biomedclip | deepdrid | NS-Fuse | 1085 | 0.008 | -0.001 | 0.016 | 0.002 |
| biomedclip | deepdrid | NS-Fuse-T | 1076 | 0.041 | -0.003 | 0.079 | 0.004 |
| biomedclip | deepdrid | NS-Joint | 1062 | 0.175 | -0.001 | 0.373 | 0.057 |
| biomedclip | internal_test | CBM-KG | 933 | -0.140 | 0.301 | 0.305 | 0.791 |
| biomedclip | internal_test | KG-Sym | 910 | 0.212 | -0.011 | 0.712 | 0.108 |
| biomedclip | internal_test | KG-Sym-T | 839 | 0.333 | -0.010 | 0.941 | 0.068 |
| biomedclip | internal_test | NS-Fuse | 1175 | 0.013 | -0.001 | 0.034 | 0.002 |
| biomedclip | internal_test | NS-Fuse-T | 1154 | 0.060 | -0.004 | 0.148 | 0.004 |
| biomedclip | internal_test | NS-Joint | 1128 | 0.216 | -0.007 | 0.566 | 0.073 |
| flair | deepdrid | CBM-KG | 1206 | 0.285 | 0.199 | 0.697 | 0.610 |
| flair | deepdrid | KG-Sym | 1574 | 0.492 | 0.014 | 0.929 | 0.027 |
| flair | deepdrid | KG-Sym-T | 974 | 0.216 | -0.019 | 0.903 | 0.080 |
| flair | deepdrid | NS-Fuse | 819 | 0.000 | 0.000 | 0.000 | 0.000 |
| flair | deepdrid | NS-Fuse-T | 819 | 0.000 | 0.000 | 0.000 | 0.000 |
| flair | deepdrid | NS-Joint | 957 | 0.565 | 0.009 | 0.967 | 0.164 |
| flair | internal_test | CBM-KG | 1213 | 0.044 | 0.333 | 0.322 | 0.652 |
| flair | internal_test | KG-Sym | 1137 | 0.331 | -0.028 | 0.805 | 0.045 |
| flair | internal_test | KG-Sym-T | 1129 | 0.199 | -0.042 | 0.791 | 0.096 |
| flair | internal_test | NS-Fuse | 1211 | 0.000 | 0.000 | 0.000 | 0.000 |
| flair | internal_test | NS-Fuse-T | 1211 | 0.000 | 0.000 | 0.000 | 0.000 |
| flair | internal_test | NS-Joint | 1211 | 0.345 | -0.019 | 0.556 | 0.028 |

## Clinical-rule consistency (reference evidence: KG-Sym-T lesion concepts)

| Encoder | Cohort | Model | Mean KG support of prediction | Violation rate (support < 0.05) |
|---|---|---|---|---|
| biomedclip | deepdrid | CBM-KG | 0.438 | 0.000 |
| biomedclip | deepdrid | KG-Sym | 0.452 | 0.000 |
| biomedclip | deepdrid | KG-Sym-T | 0.459 | 0.000 |
| biomedclip | deepdrid | NN | 0.357 | 0.002 |
| biomedclip | deepdrid | NS-Fuse | 0.359 | 0.002 |
| biomedclip | deepdrid | NS-Fuse-T | 0.366 | 0.001 |
| biomedclip | deepdrid | NS-Joint | 0.365 | 0.001 |
| biomedclip | deepdrid | ZS-Grade | 0.269 | 0.012 |
| biomedclip | internal_test | CBM-KG | 0.491 | 0.000 |
| biomedclip | internal_test | KG-Sym | 0.502 | 0.000 |
| biomedclip | internal_test | KG-Sym-T | 0.505 | 0.000 |
| biomedclip | internal_test | NN | 0.441 | 0.003 |
| biomedclip | internal_test | NS-Fuse | 0.443 | 0.003 |
| biomedclip | internal_test | NS-Fuse-T | 0.449 | 0.002 |
| biomedclip | internal_test | NS-Joint | 0.447 | 0.003 |
| biomedclip | internal_test | ZS-Grade | 0.361 | 0.005 |
| flair | deepdrid | CBM-KG | 0.280 | 0.000 |
| flair | deepdrid | KG-Sym | 0.201 | 0.000 |
| flair | deepdrid | KG-Sym-T | 0.394 | 0.000 |
| flair | deepdrid | NN | 0.316 | 0.025 |
| flair | deepdrid | NS-Fuse | 0.316 | 0.025 |
| flair | deepdrid | NS-Fuse-T | 0.316 | 0.025 |
| flair | deepdrid | NS-Joint | 0.332 | 0.000 |
| flair | deepdrid | ZS-Grade | 0.346 | 0.002 |
| flair | internal_test | CBM-KG | 0.484 | 0.000 |
| flair | internal_test | KG-Sym | 0.491 | 0.000 |
| flair | internal_test | KG-Sym-T | 0.496 | 0.000 |
| flair | internal_test | NN | 0.472 | 0.005 |
| flair | internal_test | NS-Fuse | 0.472 | 0.005 |
| flair | internal_test | NS-Fuse-T | 0.472 | 0.005 |
| flair | internal_test | NS-Joint | 0.475 | 0.004 |
| flair | internal_test | ZS-Grade | 0.463 | 0.000 |

## Zero-shot lesion-concept validity (no training): AUC for grade >= concept level

| concept /  | level /  | biomedclip / deepdrid | biomedclip / internal_test | flair / deepdrid | flair / internal_test |
|---|---|---|---|---|---|
| CWS | 2 | 0.764 | 0.816 | 0.933 | 0.943 |
| EX | 2 | 0.768 | 0.815 | 0.938 | 0.949 |
| HE | 2 | 0.709 | 0.781 | 0.94 | 0.954 |
| IRMA | 3 | 0.639 | 0.866 | 0.932 | 0.915 |
| MA | 1 | 0.642 | 0.746 | 0.864 | 0.952 |
| NV | 4 | 0.773 | 0.881 | 0.889 | 0.943 |
| PRH | 4 | 0.726 | 0.839 | 0.891 | 0.932 |
| SHE | 3 | 0.784 | 0.899 | 0.87 | 0.787 |
| VB | 3 | 0.731 | 0.881 | 0.92 | 0.864 |

## Paired bootstrap vs NN (seed 0, 1,000 resamples)

| encoder | cohort | model | vs | metric | mean_diff | ci_low | ci_high | p_one_sided |
|---|---|---|---|---|---|---|---|---|
| flair | internal_test | NS-Fuse | NN | qwk | 0 | 0 | 0 | 1 |
| flair | internal_test | NS-Fuse | NN | macro_f1 | 0 | 0 | 0 | 1 |
| flair | internal_test | NS-Fuse-T | NN | qwk | 0 | 0 | 0 | 1 |
| flair | internal_test | NS-Fuse-T | NN | macro_f1 | 0 | 0 | 0 | 1 |
| flair | internal_test | NS-Joint | NN | qwk | 0.001 | -0.0063 | 0.0075 | 0.376 |
| flair | internal_test | NS-Joint | NN | macro_f1 | 0.0139 | 0.0008 | 0.0271 | 0.02 |
| flair | internal_test | KG-Sym-T | NN | qwk | -0.0256 | -0.0409 | -0.01 | 1 |
| flair | internal_test | KG-Sym-T | NN | macro_f1 | -0.167 | -0.1947 | -0.1392 | 1 |
| flair | deepdrid | NS-Fuse | NN | qwk | 0 | 0 | 0 | 1 |
| flair | deepdrid | NS-Fuse | NN | macro_f1 | 0 | 0 | 0 | 1 |
| flair | deepdrid | NS-Fuse-T | NN | qwk | 0 | 0 | 0 | 1 |
| flair | deepdrid | NS-Fuse-T | NN | macro_f1 | 0 | 0 | 0 | 1 |
| flair | deepdrid | NS-Joint | NN | qwk | 0.1698 | 0.1312 | 0.2079 | 0 |
| flair | deepdrid | NS-Joint | NN | macro_f1 | 0.0437 | 0.0185 | 0.0682 | 0 |
| flair | deepdrid | KG-Sym-T | NN | qwk | 0.2043 | 0.1673 | 0.2431 | 0 |
| flair | deepdrid | KG-Sym-T | NN | macro_f1 | 0.0042 | -0.0236 | 0.0315 | 0.389 |
| biomedclip | internal_test | NS-Fuse | NN | qwk | 0 | 0 | 0 | 1 |
| biomedclip | internal_test | NS-Fuse | NN | macro_f1 | 0 | 0 | 0 | 1 |
| biomedclip | internal_test | NS-Fuse-T | NN | qwk | 0.0064 | -0.0026 | 0.0162 | 0.105 |
| biomedclip | internal_test | NS-Fuse-T | NN | macro_f1 | -0.0026 | -0.0168 | 0.0112 | 0.629 |
| biomedclip | internal_test | NS-Joint | NN | qwk | -0.0004 | -0.0131 | 0.0119 | 0.513 |
| biomedclip | internal_test | NS-Joint | NN | macro_f1 | -0.0133 | -0.0311 | 0.0037 | 0.935 |
| biomedclip | internal_test | KG-Sym-T | NN | qwk | -0.1074 | -0.1377 | -0.0788 | 1 |
| biomedclip | internal_test | KG-Sym-T | NN | macro_f1 | -0.1254 | -0.1561 | -0.0944 | 1 |
| biomedclip | deepdrid | NS-Fuse | NN | qwk | 0 | 0 | 0 | 1 |
| biomedclip | deepdrid | NS-Fuse | NN | macro_f1 | 0 | 0 | 0 | 1 |
| biomedclip | deepdrid | NS-Fuse-T | NN | qwk | 0.0084 | -0.0041 | 0.0222 | 0.115 |
| biomedclip | deepdrid | NS-Fuse-T | NN | macro_f1 | 0.0019 | -0.0096 | 0.0116 | 0.357 |
| biomedclip | deepdrid | NS-Joint | NN | qwk | -0.0083 | -0.0291 | 0.014 | 0.768 |
| biomedclip | deepdrid | NS-Joint | NN | macro_f1 | -0.0157 | -0.0303 | -0.0021 | 0.985 |
| biomedclip | deepdrid | KG-Sym-T | NN | qwk | -0.053 | -0.1036 | -0.0047 | 0.983 |
| biomedclip | deepdrid | KG-Sym-T | NN | macro_f1 | -0.0039 | -0.0284 | 0.0209 | 0.612 |

## 95% bootstrap CIs (seed 0)

| encoder | cohort | model | qwk_ci | macro_f1_ci | bal_acc_ci |
|---|---|---|---|---|---|
| flair | internal_test | NS-Fuse | (0.8419517789229831, 0.8743140908685656) | (0.6441512757318031, 0.6931765377336533) | (0.6603222299523613, 0.7115083815842786) |
| flair | internal_test | NS-Fuse-T | (0.8419517789229831, 0.8743140908685656) | (0.6441512757318031, 0.6931765377336533) | (0.6603222299523613, 0.7115083815842786) |
| flair | internal_test | NS-Joint | (0.8417525600657427, 0.8755903919634516) | (0.6559663688971608, 0.7078962394014815) | (0.6684900517235407, 0.7238462417248077) |
| flair | internal_test | KG-Sym-T | (0.8152007719337213, 0.8499324252743918) | (0.4847451825019459, 0.5201410754684735) | (0.5150525505952035, 0.5470961617956537) |
| flair | internal_test | KG-Sym | (0.8316762794560355, 0.8668609974689401) | (0.5905462108039061, 0.645235855876148) | (0.5840334526527777, 0.6338963447436889) |
| flair | internal_test | NN | (0.8419517789229831, 0.8743140908685656) | (0.6441512757318031, 0.6931765377336533) | (0.6603222299523613, 0.7115083815842786) |
| flair | internal_test | ZS-Grade | (0.8067824878364254, 0.8438134102792173) | (0.563811508986743, 0.6119673894604793) | (0.629680547513932, 0.6818752170591875) |
| flair | deepdrid | NS-Fuse | (0.5166266443929642, 0.5915557425200376) | (0.35124803118395465, 0.40307139473760495) | (0.3635407780763305, 0.41546352969750694) |
| flair | deepdrid | NS-Fuse-T | (0.5166266443929642, 0.5915557425200376) | (0.35124803118395465, 0.40307139473760495) | (0.3635407780763305, 0.41546352969750694) |
| flair | deepdrid | NS-Joint | (0.6934995044786595, 0.7524084634967302) | (0.39849314947963904, 0.44577947095162224) | (0.47315042957868003, 0.5177616516597678) |
| flair | deepdrid | KG-Sym-T | (0.7354791854923182, 0.7805323906307595) | (0.36055972611393583, 0.4026447487107041) | (0.418912521056853, 0.47159237904312395) |
| flair | deepdrid | KG-Sym | (0.0, 0.0022763323538771856) | (0.018487394957983194, 0.026494243283188168) | (0.2, 0.2008915636276799) |
| flair | deepdrid | NN | (0.5166266443929642, 0.5915557425200376) | (0.35124803118395465, 0.40307139473760495) | (0.3635407780763305, 0.41546352969750694) |
| flair | deepdrid | ZS-Grade | (0.7546200401372042, 0.8031512297067482) | (0.4754431217342516, 0.528781903378709) | (0.5084602904274356, 0.5685264994685569) |
| biomedclip | internal_test | NS-Fuse | (0.6674226825287718, 0.7204901511380454) | (0.496295824987453, 0.5546419268750535) | (0.4921638370406014, 0.5482332677328507) |
| biomedclip | internal_test | NS-Fuse-T | (0.6753443630537489, 0.7249180806431886) | (0.49464514808871823, 0.5495164682083108) | (0.4858227397480807, 0.5395011584896809) |
| biomedclip | internal_test | NS-Joint | (0.6667855525414333, 0.7187908804870251) | (0.4858773029031534, 0.5401026762872136) | (0.48073972774691, 0.5356098451263456) |
| biomedclip | internal_test | KG-Sym-T | (0.5544962307853599, 0.6189479614829769) | (0.3759319413160575, 0.424747151836838) | (0.3784915387833043, 0.42291400947744917) |
| biomedclip | internal_test | KG-Sym | (0.5845173994319598, 0.6437967464903915) | (0.3851470699268342, 0.4322638415889904) | (0.39001111877979433, 0.4337864330837091) |
| biomedclip | internal_test | NN | (0.6674226825287718, 0.7204901511380454) | (0.496295824987453, 0.5546419268750535) | (0.4921638370406014, 0.5482332677328507) |
| biomedclip | internal_test | ZS-Grade | (0.5395818550531425, 0.5960434661296685) | (0.2945264144025532, 0.3411606451516906) | (0.30162421623644986, 0.35062890476348557) |
| biomedclip | deepdrid | NS-Fuse | (0.337040617354451, 0.4204548365696151) | (0.24514998459260956, 0.2938417877612281) | (0.3371667194646592, 0.38585063624761956) |
| biomedclip | deepdrid | NS-Fuse-T | (0.34536214587413516, 0.4287419437250142) | (0.24647542595300387, 0.2950546309424191) | (0.3346269736511912, 0.3846016456733146) |
| biomedclip | deepdrid | NS-Joint | (0.3265077436003177, 0.4128673454074025) | (0.23053102320129995, 0.27715040160491783) | (0.325883546475787, 0.374572737308766) |
| biomedclip | deepdrid | KG-Sym-T | (0.2731462133487274, 0.3806862551153822) | (0.24362009061854276, 0.28769303189882306) | (0.297421310972104, 0.35040499920653023) |
| biomedclip | deepdrid | KG-Sym | (0.25754294965809005, 0.36349291116077775) | (0.23078532500376756, 0.27274387332912614) | (0.3022380570056651, 0.35368686799461185) |
| biomedclip | deepdrid | NN | (0.337040617354451, 0.4204548365696151) | (0.24514998459260956, 0.2938417877612281) | (0.3371667194646592, 0.38585063624761956) |
| biomedclip | deepdrid | ZS-Grade | (0.30414159846599315, 0.4091116179736799) | (0.179212830053051, 0.23024079471655562) | (0.2485140287607272, 0.314713127988816) |

## Cohorts

| encoder | cohort | n_total | n_possible_duplicates | max_cos_to_train_median | n_used | n_train | n_val | n_test |
|---|---|---|---|---|---|---|---|---|
| flair | deepdrid | 1589 | 0 | 0.5032 | 1589 | nan | nan | nan |
| flair | internal | nan | nan | nan | nan | 1.123e+04 | 2386 | 2377 |
| biomedclip | deepdrid | 1589 | 343 | 0.9718 | 1246 | nan | nan | nan |
| biomedclip | internal | nan | nan | nan | nan | 1.123e+04 | 2386 | 2377 |

## Internal test by source (seed 0)

| encoder | source | model | n | acc | macro_f1 | qwk |
|---|---|---|---|---|---|---|
| flair | aptos | ZS-Grade | 443 | 0.664 | 0.522 | 0.853 |
| flair | aptos | NN | 443 | 0.813 | 0.707 | 0.914 |
| flair | aptos | CBM-KG | 443 | 0.788 | 0.658 | 0.913 |
| flair | aptos | KG-Sym-T | 443 | 0.752 | 0.45 | 0.865 |
| flair | aptos | KG-Sym | 443 | 0.786 | 0.59 | 0.908 |
| flair | aptos | NS-Fuse | 443 | 0.813 | 0.707 | 0.914 |
| flair | aptos | NS-Fuse-T | 443 | 0.813 | 0.707 | 0.914 |
| flair | aptos | NS-Joint | 443 | 0.828 | 0.731 | 0.921 |
| flair | ddr | ZS-Grade | 1644 | 0.75 | 0.605 | 0.826 |
| flair | ddr | NN | 1644 | 0.816 | 0.659 | 0.852 |
| flair | ddr | CBM-KG | 1644 | 0.798 | 0.643 | 0.844 |
| flair | ddr | KG-Sym-T | 1644 | 0.787 | 0.523 | 0.822 |
| flair | ddr | KG-Sym | 1644 | 0.807 | 0.609 | 0.833 |
| flair | ddr | NS-Fuse | 1644 | 0.816 | 0.659 | 0.852 |
| flair | ddr | NS-Fuse-T | 1644 | 0.816 | 0.659 | 0.852 |
| flair | ddr | NS-Joint | 1644 | 0.822 | 0.671 | 0.852 |
| flair | idrid | ZS-Grade | 78 | 0.564 | 0.503 | 0.786 |
| flair | idrid | NN | 78 | 0.692 | 0.554 | 0.835 |
| flair | idrid | CBM-KG | 78 | 0.679 | 0.582 | 0.855 |
| flair | idrid | KG-Sym-T | 78 | 0.628 | 0.415 | 0.814 |
| flair | idrid | KG-Sym | 78 | 0.756 | 0.677 | 0.85 |
| flair | idrid | NS-Fuse | 78 | 0.692 | 0.554 | 0.835 |
| flair | idrid | NS-Fuse-T | 78 | 0.692 | 0.554 | 0.835 |
| flair | idrid | NS-Joint | 78 | 0.705 | 0.564 | 0.837 |
| flair | messidor2 | ZS-Grade | 212 | 0.703 | 0.639 | 0.718 |
| flair | messidor2 | NN | 212 | 0.703 | 0.653 | 0.745 |
| flair | messidor2 | CBM-KG | 212 | 0.712 | 0.655 | 0.787 |
| flair | messidor2 | KG-Sym-T | 212 | 0.755 | 0.493 | 0.826 |
| flair | messidor2 | KG-Sym | 212 | 0.769 | 0.698 | 0.819 |
| flair | messidor2 | NS-Fuse | 212 | 0.703 | 0.653 | 0.745 |
| flair | messidor2 | NS-Fuse-T | 212 | 0.703 | 0.653 | 0.745 |
| flair | messidor2 | NS-Joint | 212 | 0.689 | 0.643 | 0.745 |
| biomedclip | aptos | ZS-Grade | 443 | 0.449 | 0.327 | 0.659 |
| biomedclip | aptos | NN | 443 | 0.747 | 0.61 | 0.831 |
| biomedclip | aptos | CBM-KG | 443 | 0.691 | 0.433 | 0.788 |
| biomedclip | aptos | KG-Sym-T | 443 | 0.693 | 0.414 | 0.763 |
| biomedclip | aptos | KG-Sym | 443 | 0.693 | 0.418 | 0.767 |
| biomedclip | aptos | NS-Fuse | 443 | 0.747 | 0.61 | 0.831 |
| biomedclip | aptos | NS-Fuse-T | 443 | 0.752 | 0.597 | 0.826 |
| biomedclip | aptos | NS-Joint | 443 | 0.722 | 0.578 | 0.814 |
| biomedclip | ddr | ZS-Grade | 1644 | 0.357 | 0.304 | 0.539 |
| biomedclip | ddr | NN | 1644 | 0.678 | 0.468 | 0.666 |
| biomedclip | ddr | CBM-KG | 1644 | 0.617 | 0.413 | 0.59 |
| biomedclip | ddr | KG-Sym-T | 1644 | 0.606 | 0.39 | 0.542 |
| biomedclip | ddr | KG-Sym | 1644 | 0.619 | 0.399 | 0.573 |
| biomedclip | ddr | NS-Fuse | 1644 | 0.678 | 0.468 | 0.666 |
| biomedclip | ddr | NS-Fuse-T | 1644 | 0.684 | 0.476 | 0.678 |
| biomedclip | ddr | NS-Joint | 1644 | 0.679 | 0.464 | 0.667 |
| biomedclip | idrid | ZS-Grade | 78 | 0.526 | 0.432 | 0.738 |
| biomedclip | idrid | NN | 78 | 0.513 | 0.486 | 0.826 |
| biomedclip | idrid | CBM-KG | 78 | 0.641 | 0.46 | 0.825 |
| biomedclip | idrid | KG-Sym-T | 78 | 0.615 | 0.427 | 0.787 |
| biomedclip | idrid | KG-Sym | 78 | 0.641 | 0.456 | 0.8 |
| biomedclip | idrid | NS-Fuse | 78 | 0.513 | 0.486 | 0.826 |
| biomedclip | idrid | NS-Fuse-T | 78 | 0.538 | 0.497 | 0.833 |
| biomedclip | idrid | NS-Joint | 78 | 0.513 | 0.494 | 0.829 |
| biomedclip | messidor2 | ZS-Grade | 212 | 0.41 | 0.24 | 0.324 |
| biomedclip | messidor2 | NN | 212 | 0.575 | 0.412 | 0.479 |
| biomedclip | messidor2 | CBM-KG | 212 | 0.608 | 0.321 | 0.45 |
| biomedclip | messidor2 | KG-Sym-T | 212 | 0.594 | 0.203 | 0.361 |
| biomedclip | messidor2 | KG-Sym | 212 | 0.599 | 0.208 | 0.406 |
| biomedclip | messidor2 | NS-Fuse | 212 | 0.575 | 0.412 | 0.479 |
| biomedclip | messidor2 | NS-Fuse-T | 212 | 0.58 | 0.395 | 0.459 |
| biomedclip | messidor2 | NS-Joint | 212 | 0.575 | 0.375 | 0.498 |
