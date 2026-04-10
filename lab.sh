#!/bin/sh

set -exu

export DEB_BUILD_OPTIONS=crossbuildcanrunhostbinaries

## la grand majorités de nos packages sont indépendants de
## l' architecture de l OBC ("all")

# code Python
equivs-build edm
equivs-build camera

# ... destiné uniquement au OBC TranzCom (Buster)
equivs-build hsupa-handler
# ... destiné uniquement au OBC Kontron (Trixie)
equivs-build kontron-4g

# firmwares arhmf ou autres destinés à des tierces parties
equivs-build switch-audio-firmware
equivs-build vnas4200-firmware


## certains packages "any" ont été compilés pour i386 et amd64

# par nous-même
equivs-build concentrator
equivs-build concentrator --arch i386

# par une tierce partie
equivs-build aco-concent-522001
equivs-build aco-concent-522001 --arch i386


## d'autres packages ne resteront disponible qu en i386
## car le coup de portage serait prohibitif face aux gains

# par nous-même
equivs-build stub --arch i386 # interdépendant de SAE
equivs-build stibis-api --arch i386 # code qui fait peur
equivs-build tcn-handler --arch i386

# par une tierce partie
equivs-build sae --arch i386
