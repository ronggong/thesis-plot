import numpy as np
import matplotlib.style
import matplotlib as mpl
mpl.style.use('classic')
import matplotlib.pyplot as plt

fontsize = 15


def plot_two_spectro_onsets(mfcc0,
                            mfcc1,
                            hopsize_t,
                            groundtruth_onset0,
                            groundtruth_onset1):

    plt.figure(figsize=(16, 6))

    ax1 = plt.subplot(2, 1, 1)
    y = np.arange(0, 80)
    x = np.arange(0, mfcc0.shape[0]) * hopsize_t
    plt.pcolormesh(x, y, np.transpose(mfcc0))
    for gs, label in groundtruth_onset0:
        plt.axvline(gs, color='r', linewidth=2)
        plt.text(gs, 81, label, fontsize=fontsize)

    ax1.set_ylabel('Teacher', fontsize=fontsize)
    ax1.axis('tight')

    ax2 = plt.subplot(2, 1, 2)
    x = np.arange(0, mfcc1.shape[0]) * hopsize_t
    plt.pcolormesh(x, y, np.transpose(mfcc1))
    for gs, label in groundtruth_onset1:
        plt.axvline(gs, color='r', linewidth=2)
        plt.text(gs, 81, label, fontsize=fontsize)

    ax2.set_ylabel('Student', fontsize=fontsize)
    ax2.axis('tight')
    plt.xlabel('time (s)')

    plt.savefig('ch2_pro_amateur.png', bbox_inches='tight')

    # plt.show()


def plot_one_spectro_syllable_phoneme(mfcc,
                                      hopsize_t,
                                      groundtruth_syllable_onset,
                                      groundtruth_phoneme_onset,
                                      figname):

    plt.figure(figsize=(16, 3))

    ax1 = plt.subplot(1, 1, 1)
    y = np.arange(0, 80)
    x = np.arange(0, mfcc.shape[0]) * hopsize_t
    plt.pcolormesh(x, y, np.transpose(mfcc))

    for gp, label in groundtruth_phoneme_onset:
        plt.axvline(gp, color='k', linewidth=1, linestyle="--")
        plt.text(gp, 88, label, fontsize=fontsize)

    for gs, label in groundtruth_syllable_onset:
        plt.axvline(gs, color='r', linewidth=2)
        plt.text(gs, 81, label, fontsize=fontsize)

    ax1.set_ylabel('Mel bands', fontsize=fontsize)
    ax1.set_xlabel('time (s)')
    ax1.axis('tight')

    plt.savefig(figname, bbox_inches='tight')

    # plt.show()