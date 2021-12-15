using System;
using System.IO;
using System.Security.Cryptography;

namespace P1_2
{
    class Program
    {
        static void Main(string[] args)
        {
            string plaintext = args[0];
            string ciphertext = args[1];

            DateTime origin = new DateTime(1970, 1, 1);
            DateTime startTime = new DateTime(2020, 7, 3, 11, 0, 0);
            DateTime endTime = new DateTime(2020, 7, 4, 11, 0, 0);
            int startMinutes = (int)startTime.Subtract(origin).TotalMinutes;
            int endMinutes = (int)endTime.Subtract(origin).TotalMinutes;

            for (int minutes = startMinutes; minutes <= endMinutes; minutes++)
            {
                Random rng = new Random(minutes);
                byte[] key = BitConverter.GetBytes(rng.NextDouble());
                string candidateText = Encrypt(key, plaintext);
                if (candidateText == ciphertext)
                {
                    Console.WriteLine(minutes);
                    break;
                }
            }
        }

        private static string Encrypt(byte[] key, string secretString)
        {
            DESCryptoServiceProvider csp = new DESCryptoServiceProvider();
            MemoryStream ms = new MemoryStream();
            CryptoStream cs = new CryptoStream(ms,
                csp.CreateEncryptor(key, key), CryptoStreamMode.Write);
            StreamWriter sw = new StreamWriter(cs);
            sw.Write(secretString);
            sw.Flush();
            cs.FlushFinalBlock();
            sw.Flush();
            return Convert.ToBase64String(ms.GetBuffer(), 0, (int)ms.Length);
        }
    }
}
