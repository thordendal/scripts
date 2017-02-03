#!/bin/bash

if [ -z "$1" ]; then
	DOMAINS=
	while IFS= read -r LINE || [[ -n "$LINE" ]]; do
	DOMAINS="$DOMAINS \
	$LINE"
	done
	for domain in $DOMAINS; do
		LOOKUP=$(echo | openssl s_client \
			-showcerts \
			-servername $domain \
			-connect $domain:443 2>/dev/null | \
			openssl x509 \
			-inform pem \
			-noout \
			-text | \
			grep CPS | \
			awk '{print $2}')
		if [ $LOOKUP == "http://cps.letsencrypt.org" ]; then
			echo $domain
		fi
	done
	exit 0
elif [ $1 == "--help" ] || [ $1 == "-h" ]; then
echo "Usage: $0 [domain]
If no domain is given as single argument, this script will read domains from
stdin, one domain per line
Note that if working in multi-domain mode, script will print only domains
that have set up Letsencrypt SSL"
exit 0
else
	LOOKUP=$(echo | openssl s_client \
		-showcerts \
		-servername $1 \
		-connect $1:443 2>/dev/null | \
		openssl x509 \
		-inform pem \
		-noout \
		-text 2>/dev/null | \
		grep CPS | \
		awk '{print $2}')
	if [ ! -z $LOOKUP ] && [ $LOOKUP == "http://cps.letsencrypt.org" ]; then
		echo $1 has Letsencrypt cert
		exit 0
	else
		echo $1 has not Letsencrypt cert \(or isn\'t set up to use it\)
		exit 1
	fi
fi
