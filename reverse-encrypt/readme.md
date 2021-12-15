# Find Time of Encryption

## Purpose

We know that a certain plain text message was encrypted with a key that's the number of minutes since origin. We also happen to know that the encryption was done between 7/3/2020 11:00 AM and 7/4/2020 11:00 AM. Typically, keys are seeded with a resolution of a millisecond or less. In this case, we see how vulnerable DES is when we know that the key is within a set of minutes.

## How To Use

The program takes two arguments: plaintext and ciphertext. It will then output the number of minutes that had elapsed at the time of encryption from the date specified.

## Dependencies

The program uses **C#**. The encryption uses ``DESCryptoServiceProvider`` of the ``System.Security.Cryptography`` library.