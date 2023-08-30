# The `filter` SigMF Extension Namespace v0.0.1

## Description

This document defines the `filter` extension namespace for the Signal
Metadata Format (SigMF) specification. This extension namespace defines how to
describe the transmit filter used in a wireless communications system.

## Conventions Used in this Document

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”,
“SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

JSON keywords are used as defined in [ECMA-404](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf).

Augmented Backus-Naur form (ABNF) is used as defined by [RFC
5234](https://tools.ietf.org/html/rfc5234) and updated by [RFC
7405](https://tools.ietf.org/html/rfc7405).

Fields defined as "human-readable", a "string", or simply as "text" shall be
treated as plaintext where whitespace is significant, unless otherwise
specified.

## Specification

This specification defines an extension `filter` namespace
that can be used in SigMF `annotations` to describe the transmit filter in a wireless communications
system.

### Annotations

This extension adds the following field to the `annotations` global SigMF object:

|name|required|type|description|
|----|--------------|-------|-----------|
|filter|false|object|Describes the transmit filter of the communications system.|

#### The `filter` Object

`filter` objects contain name/value pairs that describe the modulations of communications systems. These objects MAY contain the following pairs:

|name|required|type|
|----|--------------|-------|
|`type`|false|string|
|`sps`|false|list|
|`rolloff`|false|list|
|`delay`|false|int|
|`dt`|false|uint|

###### The `type` Pair

The `type` name can have the following values:

|value|description|
|----|-------|
|`rrc`|root raised cosine filter|

###### The `sps` Pair

The `sps` name specifies the sampling rate of the signal, and must be a list of the form [start, stop, step]. For example, a sps value of [2, 8, 2] would specify sps values of [2, 4, 6, 8]. 

###### The `rolloff` pair

The `rolloff` name specifies the rrc rolloff factor (a.k.a. beta), and  must be a list of the form [start, stop, step]. For example, a rolloff value of [0.34, 0.36, 0.01] would specify rolloff values of [0.34, 0.35, 0.36].

###### The `delay` pair

The `delay` name specifies the filter delay, and must be an integer value greater than 0. Note that this delay has been compensated for in the data generation, and the filter ramp up has been stripped off.

###### The `dt` Pair

The `dt` name specifies any timing offset, and must be a list of the form [start, stop, step], where the start/stop are the number of symbols offset which can be float valued. For example, [0.0, 1.0, 0.1] specifies an offset of [0.0, 0.1, 0.2, ..., 1.0].

## Examples

Here is an example of a relatively simple filter label, which describes a signal transmitted using a root-raised cosine filter with a rolloff factor of 0.35, a filter delay of 3 symbols, and no timing offset, sampled at 8 samples per symbol:

    "filter": {
        "type": "rrc",
        "sps": [8, 8, 1],
        "rolloff": [0.35, 0.35, 0.01],
        "delay": 3,
	"dt":[0.0, 0.0, 0.1]
    }

Here is a more complex example that describes an LTE 5 MHz SC-OFDMA downlink:

    "modulation": {
        "type": "digital",
        "class": "qam",
        "carrier_variant": "single_carrier",
        "order": 16,
        "multiple_access": "ofdma",
        "bandwidth": 5000000.0,
        "system": "LTE Release 12"
    }

