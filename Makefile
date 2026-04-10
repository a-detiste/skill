#!/bin/make

export DEB_BUILD_OPTIONS=crossbuildcanrunhostbinaries

debs: aco-concent-522001_1.0_amd64.deb  camera_1.0_all.deb  concentrator_1.0_i386.deb  hsupa-handler_1.0_all.deb  sae_1.0_i386.deb stub_1.0_i386.deb tch-handler_1.0_i386.deb aco-concent-522001_1.0_i386.deb   concentrator_1.0_amd64.deb  edm_1.0_all.deb            kontron-4g_1.0_all.deb     stibis-api_1.0_i386.deb  switch-audio-firmware_1.0_all.deb  vnas4200-firmware_1.0_all.deb

## la grand majorités de nos packages sont indépendants de
## l' architecture de l OBC ("all")

# code Python
edm_1.0_all.deb: packages/edm
	equivs-build packages/edm

camera_1.0_all.deb: packages/camera
	equivs-build packages/camera

# ... destiné uniquement au OBC TranzCom (Buster)
hsupa-handler_1.0_all.deb: packages/hsupa-handler
	equivs-build packages/hsupa-handler
# ... destiné uniquement au OBC Kontron (Trixie)
kontron-4g_1.0_all.deb: packages/kontron-4g
	equivs-build packages/kontron-4g

# firmwares arhmf ou autres destinés à des tierces parties
switch-audio-firmware_1.0_all.deb: packages/switch-audio-firmware
	equivs-build packages/switch-audio-firmware
vnas4200-firmware_1.0_all.deb: packages/vnas4200-firmware
	equivs-build packages/vnas4200-firmware


## certains packages "any" ont été compilés pour i386 et amd64

# par nous-même
concentrator_1.0_amd64.deb: packages/concentrator
	equivs-build packages/concentrator

concentrator_1.0_i386.deb: packages/concentrator
	equivs-build packages/concentrator --arch i386

# par une tierce partie
aco-concent-522001_1.0_amd64.deb: packages/aco-concent-522001
	equivs-build packages/aco-concent-522001

aco-concent-522001_1.0_i386.deb: packages/aco-concent-522001
	equivs-build packages/aco-concent-522001 --arch i386

## d'autres packages ne resteront disponible qu en i386
## car le coup de portage serait prohibitif face aux gains

# par nous-même
stub_1.0_i386.deb: packages/stub
	equivs-build packages/stub --arch i386 # interdépendant de SAE
stibis-api_1.0_i386.deb: packages/stibis-api
	equivs-build packages/stibis-api --arch i386 # code qui fait peur
tch-handler_1.0_i386.deb: packages/tcn-handler
	equivs-build packages/tcn-handler --arch i386

# par une tierce partie
sae_1.0_i386.deb: packages/sae
	equivs-build packages/sae --arch i386

# tout doit provenir du .deb
#rm -vf *.buildinfo *.changes
