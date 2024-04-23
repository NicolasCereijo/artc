# artc-core
## Metrics and their comparisons
### Comparisons

- Pearson correlation

![\color{white}\rho_{X,Y}=\frac{{\sum_{i=1}^{n}(X_i-\bar{X})(Y_i-\bar{Y})}}{{\sqrt{\sum_{i=1}^{n}(X_i-\bar{X})^2\sum_{i=1}^{n}(Y_i-\bar{Y})^2}}}](https://latex.codecogs.com/svg.image?\color{white}\rho_{X,Y}=\frac{{\sum_{i=1}^{n}(X_i-\bar{X})(Y_i-\bar{Y})}}{{\sqrt{\sum_{i=1}^{n}(X_i-\bar{X})^2\sum_{i=1}^{n}(Y_i-\bar{Y})^2}}})

- Cosine Similarity

![\color{white}similarity=\frac{A\cdot&space;B}{\left\|\left\|A\right\|\right\|\left\|\left\|B\right\|\right\|}](https://latex.codecogs.com/svg.image?\color{white}similarity=\frac{A\cdot&space;B}{\left\|\left\|A\right\|\right\|\left\|\left\|B\right\|\right\|})

- Normalized relative difference

![\color{white}nrd=1-\frac{{|x-y|}}{{\max(x,y)}}](https://latex.codecogs.com/svg.image?\color{white}nrd=1-\frac{{|x-y|}}{{\max(x,y)}})

### Metrics
- chroma ─> Pearson correlation
- energy envelope ─> Pearson correlation
- mfcc ─> Cosine Similarity
- rhythm ─> Normalized relative difference
- spectral contrast ─> Pearson correlation
- spectrogram ─> Cosine Similarity
- zero crossing rate ─> Normalized relative difference
