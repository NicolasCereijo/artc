# artc-core
## Metrics and their comparisons
### Comparisons
- Pearson correlation
\[
\rho_{X,Y} = \frac{{\sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}}{{\sqrt{\sum_{i=1}^{n} (X_i - \bar{X})^2 \sum_{i=1}^{n} (Y_i - \bar{Y})^2}}}
\]
- Cosine Similarity
\[
\text{similarity} = \frac{{A \cdot B}}{{\|A\| \|B\|}}
\]
- Normalized relative difference
\[
\text{normalized\_difference} = 1 - \frac{{|x - y|}}{{\max(x, y)}}
\]
### Metrics
- chroma ─> Pearson correlation
- energy envelope ─> Pearson correlation
- mfcc ─> Cosine Similarity
- rhythm ─> Normalized relative difference
- spectral contrast ─> Pearson correlation
- spectrogram ─> Cosine Similarity
- zero crossing rate ─> Normalized relative difference
