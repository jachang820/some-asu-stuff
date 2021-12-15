# Online Birthday Attack of MD5 Hash

## Purpose

MD5 is a cryptographically broken 128-bit hash. This program generates MD5 hashes from random 10-character strings until it finds a collision using the birthday attack.

## How To Use

The program takes one argument: a salt that will prevent the attack from being precomputed. Once it finds a collision, it will output the two strings that caused the collision.

## Dependencies

The program uses **C#**. The hash uses ``MD5`` of the ``System.Security.Cryptography`` library.