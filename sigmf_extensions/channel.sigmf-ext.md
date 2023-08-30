# The `channel` SigMF Extension Namespace v0.0.1

## Description

This document defines the `channel` extension namespace for the Signal
Metadata Format (SigMF) specification. This extension namespace defines how to
describe the channel through which a signal has travelled.

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

This specification defines an extension `channel` namespace
that can be used in SigMF `annotations` to describe propagation channels.

### Annotations

This extension adds the following field to the `annotations` global SigMF object:

|name|required|type|description|
|----|--------------|-------|-----------|
|channel|false|object|Describes a propagation channel.|

#### The `modulation` Object

`channel` objects contain name/value pairs that describe the channel through which the received signal has propagated. These objects MAY contain the following pairs:

|name|required|type|
|----|--------------|-------|
|`type`|false|string|
|`snr`|false|float|
|`fo`|false|float|
|`po`|false|float|

###### The `type` Pair

The `type` name specifies the type of channel the signal propagated through and can have the following values:

|value|description|
|----|-------|
|`awgn`|additive white gaussian noise channel|

###### The `snr` Pair

The `snr` name has a float value that describes the signal to noise ratio of the received signal in dB. 

###### The `fo` Pair

The `fo` name has a float value that describes the frequency offset of the received signal, divided by pi (i.e. fo = 0.1 corresponds to a frequency offset of 0.1 * pi). 

###### The `po` Pair

The `po` name has a float value that describes the phase offset of the received signal, divided by pi (i.e. po = 0.1 corresponds to a phase offset of 0.1 * pi).

## Examples

Here is an example of a relatively simple channel label, which describes a signal which propagated thorough an awgn channel and was received with a 10dB signal to noise ratio, a frequency offset of 0.1 * pi radians/sample, and no phase offset:

    "channel": {
        "type": "awgn",
        "snr": 10.0,
        "fo": 0.1,
        "po": 0.0
    }


