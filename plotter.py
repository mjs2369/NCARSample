# plot_bestfit is defined within the lc_fitter class.
def plot_bestfit(self, nbins=10, phase=True, title=""):

    f, (ax_lc, ax_res) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

    if phase:
        ax_res.set_xlabel('Phase')

        ecks = self.phase

    else:
        ax_res.set_xlabel('Time [day]')

        ecks = self.time


    # clip plot to get rid of white space
    ax_res.set_xlim([min(ecks), max(ecks)])
    ax_lc.set_xlim([min(ecks), max(ecks)])

    # making borders and tick labels black
    ax_lc.spines['bottom'].set_color('black')
    ax_lc.spines['top'].set_color('black')
    ax_lc.spines['right'].set_color('black')
    ax_lc.spines['left'].set_color('black')
    ax_lc.tick_params(axis='x', colors='black')
    ax_lc.tick_params(axis='y', colors='black')

    ax_res.spines['bottom'].set_color('black')
    ax_res.spines['top'].set_color('black')
    ax_res.spines['right'].set_color('black')
    ax_res.spines['left'].set_color('black')
    ax_res.tick_params(axis='x', colors='black')
    ax_res.tick_params(axis='y', colors='black')

    # residual plot
    ax_res.errorbar(ecks, self.residuals / np.median(self.data), yerr=self.detrendederr, color='gray',
                    marker='o', markersize=5, linestyle='None', mec='None', alpha=0.75)
    ax_res.plot(ecks, np.zeros(len(ecks)), 'r-', lw=2, alpha=1, zorder=100)
    ax_res.set_ylabel('Residuals')
    ax_res.set_ylim([-3 * np.nanstd(self.residuals / np.median(self.data)),
                     3 * np.nanstd(self.residuals / np.median(self.data))])
    
    # plotting the final lightcurve model calculated in transit() method that also belongs to the lc_fitter class.
    ax_lc.plot(ecks, self.transit, 'r', zorder=1000, lw=2)

    ax_lc.set_ylabel('Relative Flux')
    ax_lc.get_xaxis().set_visible(False)

    # binner() is a method previously defined in EXOTIC - condenses multiple data points into one
    # reduces size of dataset to imporove plot legibility and reduce runtime
    # increases signal to noise ratio at each data point by reducing the statistical significance of error values 
    ax_res.errorbar(binner(ecks, len(self.residuals) // 10),
                    binner(self.residuals / np.median(self.data), len(self.residuals) // 10),
                    yerr=
                    binner(self.residuals / np.median(self.data), len(self.residuals) // 10, self.detrendederr)[
                        1],
                    fmt='s', ms=5, mfc='b', mec='None', ecolor='b', zorder=10)
    ax_lc.errorbar(binner(ecks, len(ecks) // 10),
                   binner(self.detrended, len(self.detrended) // 10),
                   yerr=
                   binner(self.residuals / np.median(self.data), len(self.residuals) // 10, self.detrendederr)[
                       1],
                   fmt='s', ms=5, mfc='b', mec='None', ecolor='b', zorder=10)

    # remove vertical whitespace
    f.subplots_adjust(hspace=0)

    return f,(ax_lc, ax_res)
