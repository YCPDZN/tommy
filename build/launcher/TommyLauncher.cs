// Tommy.exe: unpacks the game (page, audio, images) into %LOCALAPPDATA%\Tommy, serves it from a tiny
// web server on 127.0.0.1 (the page fetches audio and reads image pixels, which file:// pages may not do),
// and opens it in a chromeless Microsoft Edge app window. The exe exits when that window closes.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Win32;

[assembly: AssemblyTitle("Tommy")]
[assembly: AssemblyProduct("Tommy")]
[assembly: AssemblyVersion("1.0.0.0")]

static class TommyLauncher
{
    static string root;

    [STAThread]
    static void Main()
    {
        try
        {
            root = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Tommy", "game");
            Unpack();

            var listener = new TcpListener(IPAddress.Loopback, 0);
            listener.Start();
            int port = ((IPEndPoint)listener.LocalEndpoint).Port;
            var server = new Thread(() => Serve(listener)) { IsBackground = true };
            server.Start();

            string url = "http://127.0.0.1:" + port + "/index.html";
            string edge = FindEdge();
            if (edge == null)
            {
                Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
                MessageBox.Show("Tommy is running in your browser. Keep this message open while you play, then click OK to stop.", "Tommy");
                return;
            }
            string profile = Path.Combine(Path.GetDirectoryName(root), "profile");
            var p = Process.Start(new ProcessStartInfo(edge,
                "--app=\"" + url + "\" --window-size=1280,760 --user-data-dir=\"" + profile + "\" --no-first-run --no-default-browser-check --autoplay-policy=no-user-gesture-required")
                { UseShellExecute = false });
            p.WaitForExit();
        }
        catch (Exception e)
        {
            MessageBox.Show("Tommy could not start:\n\n" + e.Message, "Tommy", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    // every embedded resource is named by its path in the game folder, e.g. "audio/GF1.mp3"
    static void Unpack()
    {
        var asm = Assembly.GetExecutingAssembly();
        foreach (string name in asm.GetManifestResourceNames())
        {
            string path = Path.Combine(root, name.Replace('/', Path.DirectorySeparatorChar));
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            using (Stream s = asm.GetManifestResourceStream(name))
            using (FileStream f = File.Create(path))
                s.CopyTo(f);
        }
    }

    static readonly Dictionary<string, string> Types = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
    {
        { ".html", "text/html; charset=utf-8" }, { ".js", "text/javascript" }, { ".css", "text/css" },
        { ".mp3", "audio/mpeg" }, { ".jpg", "image/jpeg" }, { ".png", "image/png" }, { ".txt", "text/plain" }, { ".json", "application/json" },
    };

    static void Serve(TcpListener listener)
    {
        while (true)
        {
            TcpClient c;
            try { c = listener.AcceptTcpClient(); } catch { return; }
            ThreadPool.QueueUserWorkItem(_ => Handle(c));
        }
    }

    static void Handle(TcpClient c)
    {
        using (c)
        using (NetworkStream ns = c.GetStream())
        {
            try
            {
                var reader = new StreamReader(ns, Encoding.ASCII, false, 1024, true);
                string line = reader.ReadLine();
                if (line == null) return;
                while (!string.IsNullOrEmpty(reader.ReadLine())) { }
                string[] parts = line.Split(' ');
                string rel = parts.Length > 1 ? Uri.UnescapeDataString(parts[1].Split('?')[0]).TrimStart('/') : "";
                if (rel == "") rel = "index.html";
                string full = Path.GetFullPath(Path.Combine(root, rel.Replace('/', Path.DirectorySeparatorChar)));
                byte[] body; string status, type;
                if (full.StartsWith(root, StringComparison.OrdinalIgnoreCase) && File.Exists(full))
                {
                    body = File.ReadAllBytes(full); status = "200 OK";
                    if (!Types.TryGetValue(Path.GetExtension(full), out type)) type = "application/octet-stream";
                }
                else { body = Encoding.UTF8.GetBytes("Not found"); status = "404 Not Found"; type = "text/plain"; }
                byte[] head = Encoding.ASCII.GetBytes("HTTP/1.1 " + status + "\r\nContent-Type: " + type + "\r\nContent-Length: " + body.Length + "\r\nCache-Control: no-cache\r\nConnection: close\r\n\r\n");
                ns.Write(head, 0, head.Length);
                if (parts[0] != "HEAD") ns.Write(body, 0, body.Length);
            }
            catch { }
        }
    }

    static string FindEdge()
    {
        foreach (RegistryKey hive in new[] { Registry.CurrentUser, Registry.LocalMachine })
            using (RegistryKey k = hive.OpenSubKey(@"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"))
            {
                string p = k == null ? null : k.GetValue("") as string;
                if (!string.IsNullOrEmpty(p) && File.Exists(p)) return p;
            }
        foreach (string pf in new[] { Environment.GetEnvironmentVariable("ProgramFiles(x86)"), Environment.GetEnvironmentVariable("ProgramFiles") })
        {
            if (string.IsNullOrEmpty(pf)) continue;
            string p = Path.Combine(pf, @"Microsoft\Edge\Application\msedge.exe");
            if (File.Exists(p)) return p;
        }
        return null;
    }
}
