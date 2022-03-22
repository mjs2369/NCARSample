# plot_bestfit is a method previously defined within the lc_fitter class.
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

    correctedSTD = np.std(self.residuals / np.median(self.data))
    ax_lc.errorbar(ecks, self.detrended, yerr=self.detrendederr, ls='none',
                   marker='o', color='gray', markersize=5, mec='None', alpha=0.75)
    ax_lc.plot(ecks, self.transit, 'r', zorder=1000, lw=2)

    ax_lc.set_ylabel('Relative Flux')
    ax_lc.get_xaxis().set_visible(False)

   ## binner() is a method previously defined in EXOTIC - condenses 10 pixels into 1
   ## reduces the runtime of imaging processing, reduces the statistical significange of error values 
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

def plot_triangle(self):
    fig,axs = dynesty.plotting.cornerplot(self.results, labels=list(self.bounds.keys()), quantiles_2d=[0.4,0.85], smooth=0.015, show_titles=True,use_math_text=True, title_fmt='.2e',hist2d_kwargs={'alpha':1,'zorder':2,'fill_contours':False})
    dynesty.plotting.cornerpoints(self.results, labels=list(self.bounds.keys()), fig=[fig,axs[1:,:-1]],plot_kwargs={'alpha':0.1,'zorder':1,} )
    return fig, axs
