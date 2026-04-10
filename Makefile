#!/bin/make

export DEB_BUILD_OPTIONS=crossbuildcanrunhostbinaries

debs: aco-concent-522001_1.0_amd64.deb  camera_1.0_all.deb  concentrator_1.0_i386.deb  hsupa-handler_1.0_all.deb  sae_1.0_i386.deb stub_1.0_i386.deb tch-handler_1.0_i386.deb aco-concent-522001_1.0_i386.deb   concentrator_1.0_amd64.deb  edm_1.0_all.deb            kontron-4g_1.0_all.deb     stibis-api_1.0_i386.deb  switch-audio-firmware_1.0_all.deb  vnas4200-firmware_1.0_all.deb

## la grand majorités de nos packages sont indépendants de
## l' architecture de l OBC ("all")

# code Python
edm_1.0_all.deb: edm
	equivs-build edm

camera_1.0_all.deb: camera
	equivs-build camera

# ... destiné uniquement au OBC TranzCom (Buster)
hsupa-handler_1.0_all.deb: hsupa-handler
	equivs-build hsupa-handler
# ... destiné uniquement au OBC Kontron (Trixie)
kontron-4g_1.0_all.deb: kontron-4g
	equivs-build kontron-4g

# firmwares arhmf ou autres destinés à des tierces parties
switch-audio-firmware_1.0_all.deb: switch-audio-firmware
	equivs-build switch-audio-firmware
vnas4200-firmware_1.0_all.deb: vnas4200-firmware
	equivs-build vnas4200-firmware


## certains packages "any" ont été compilés pour i386 et amd64

# par nous-même
concentrator_1.0_amd64.deb:
	equivs-build concentrator

concentrator_1.0_i386.deb:
	equivs-build concentrator --arch i386

# par une tierce partie
aco-concent-522001_1.0_amd64.deb: aco-concent-522001
	equivs-build aco-concent-522001

aco-concent-522001_1.0_i386.deb: aco-concent-522001
	equivs-build aco-concent-522001 --arch i386

## d'autres packages ne resteront disponible qu en i386
## car le coup de portage serait prohibitif face aux gains

# par nous-même
stub_1.0_i386.deb: stub
	equivs-build stub --arch i386 # interdépendant de SAE
stibis-api_1.0_i386.deb: stibis-api
	equivs-build stibis-api --arch i386 # code qui fait peur
tch-handler_1.0_i386.deb: tcn-handler
	equivs-build tcn-handler --arch i386

# par une tierce partie
sae_1.0_i386.deb: sae
	equivs-build sae --arch i386

# tout doit provenir du .deb
#rm -vf *.buildinfo *.changes
