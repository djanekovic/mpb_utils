import matplotlib.pyplot as plt

def plot(tm_freqs, tm_gaps, te_freqs, te_gaps, limit=1, name="plot.pdf", save=False):

    plt.style.use('seaborn-white')
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig, ax = plt.subplots()
    x = range(len(tm_freqs))

    # Plot bands
    ax.plot(tm_freqs, label = "TM mod", color='blue')
    ax.plot(te_freqs, label = "TE mod", color='red')
    ax.set_ylim([0, limit])
    ax.set_xlim([x[0], x[-1]])

    # Plot gaps
    full_band_gap = []

    # check if there are any full band gaps
    for tmgap in tm_gaps:
        for tegap in te_gaps:
            if tmgap[2] < tegap[1] or tegap[2] < tmgap[1] or tegap[0] < 1 or tmgap[0] < 1:
                continue
            if tmgap[1] < tegap[1] and tmgap[2] > tegap[2]:
                #ax.fill_between(x, tegap[1], tegap[2], color='yellow', linewidth=0.0)
                full_band_gap.append((tegap[1], tegap[2]))
            elif tmgap[1] < tegap[1] and tmgap[2] < tegap[2]:
                #ax.fill_between(x, tegap[1], tmgap[2], color='yellow', linewidth=0.0)
                full_band_gap.append((tegap[1], tmgap[2]))
            elif tmgap[1] > tegap[1] and tmgap[2] > tegap[2]:
                #ax.fill_between(x, tmgap[1], tegap[2], color='yellow', linewidth=0.0)
                full_band_gap.append((tmgap[1], tegap[2]))
            elif tmgap[1] > tegap[1] and tmgap[2] < tegap[2]:
                #ax.fill_between(x, tmgap[1], tmgap[2], color='yellow', linewidth=0.0)
                full_band_gap.append((tmgap[1], tmgap[2]))

    # if there are any full band gaps plot those and not TE/TM
    if len(full_band_gap):
        for gaps in full_band_gap:
            ax.fill_between(x, gaps[0], gaps[1], color='yellow', linewidth=0.0)
    else:
        for tmgap, tegap in zip(tm_gaps, te_gaps):
            if tmgap[0] > 1:
                ax.fill_between(x, tmgap[1], tmgap[2], color='blue', alpha=0.4, linewidth=0.0)
            if tegap[0] > 1:
    	        ax.fill_between(x, tegap[1], tegap[2], color='red', alpha=0.4, linewidth=0.0)


    # Plot labels
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    points_in_between = (len(tm_freqs) - 4) / 3
    tick_locs = [i*points_in_between+i for i in range(4)]
    tick_labs = [r'$\Gamma$', 'X', 'M', r'$\Gamma$']
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labs, size=16)

    if not save:
        plt.show()
    else:
        plt.savefig(name, bbox_inches='tight')
