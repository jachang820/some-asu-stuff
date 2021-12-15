using System;
using System.Security.Cryptography;
using System.Text;
using System.Collections.Generic;

namespace P2
{
    class Program
    {
        static void Main(string[] args)
        {
            Dictionary<string, string> dict = new Dictionary<string, string>();
            Random rng = new Random();

            while (true)
            {
                string source = RandomWord(rng);
                byte[] sourceBytes = AddSalt(source, args[0]);
                string hash = GetHash(sourceBytes);
                if (!dict.ContainsKey(hash))
                {
                    dict.Add(hash, source);
                    //Console.WriteLine($"{source} generates {hash}");
                }
                else
                {
                    string firstWord = dict[hash];
                    string secondWord = source;
                    if (firstWord != secondWord)
                    {
                        Console.WriteLine(firstWord + "," + secondWord);
                        break;
                    }
                }
            }
        }

        static byte[] AddSalt(string source, string salt)
        {
            byte saltByte = Convert.ToByte(salt, 16);
            byte[] sourceBytes = Encoding.UTF8.GetBytes(source);
            Array.Resize(ref sourceBytes, sourceBytes.Length + 1);
            sourceBytes[sourceBytes.Length - 1] = saltByte;
            return sourceBytes;
        }

        static string GetHash(byte[] source)
        {
            const int TruncatedLength = 5;
            using (MD5 md5 = MD5.Create())
            {
                byte[] data = md5.ComputeHash(source);
                byte[] truncated = new byte[TruncatedLength];
                Array.Copy(data, truncated, TruncatedLength);
                string hash = BitConverter.ToString(truncated);
                return hash;
            }
        }

        static string RandomWord(Random rng)
        {
            var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            var word = new char[10];

            for (int i = 0; i < word.Length; i++)
            {
                word[i] = chars[rng.Next(chars.Length)];
            }

            return new String(word);
        }
    }
}
