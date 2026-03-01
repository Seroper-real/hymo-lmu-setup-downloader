# HYMO Setup Downloader for Le Mans Ultimate

🇮🇹 [Leggi questo README in Italiano](readme.it.md)

 <p align="center">
  <a href="https://github.com/Seroper-real/hymo-lmu-setup-downloader/releases/latest/download/hymo-lmu-setup-downloader_Windows.zip">
    <img src="https://img.shields.io/github/v/release/Seroper-real/hymo-lmu-setup-downloader?label=DOWNLOAD&style=for-the-badge&color=brightgreen" alt="Download">
  </a>
</p>

## Introduction

This project was created **purely for convenience**.

Its goal is to automate the download and installation of **TrackTitan** setups for *Le Mans Ultimate*, avoiding the need to manually download each setup from the website.

⚠️ **Important notice**

- This tool **does not bypass paywalls or limitations**
- A **valid TrackTitan account with an active subscription** is required
- Data is retrieved using the **same APIs used by the official TrackTitan web app**
- Authentication tokens must be **manually obtained via browser**

This project:

- Is **not affiliated with TrackTitan**
- Is **not supported or endorsed by TrackTitan**
- Is intended **for personal use only**

Without an active subscription, this tool **will not work**.

---

## Requirements

- A valid TrackTitan account with an active LMU setups subscription
- Windows PC
- Le Mans Ultimate installed

---

## Installation

### Step 1 – Download

1. [Download](https://github.com/Seroper-real/hymo-lmu-setup-downloader/releases/latest/download/hymo-lmu-setup-downloader_Windows.zip) the `.zip` file
2. Extract the contents to a folder of your choice

⚠️ **Recommended**

It is strongly recommended **not to delete or move the installation folder** after first use.

The program keeps a **history of already downloaded setups**, allowing it to:

- avoid downloading the same setups again
- download only **new or updated setups**
- resume correctly after closing or restarting the app

If the folder is deleted, the history will be lost and downloads will restart from scratch.

---

## Usage

### Step 2 – Get tokens from the browser

1. Log in to https://app.tracktitan.io
2. Open the browser developer tools
   - Windows/Linux: `F12` or `Ctrl + Shift + I`
   - macOS: `Cmd + Option + I`
3. Open the **Console** tab

### Step 3 – Paste the script

Paste **this single line** into the console and press Enter:

```
(()=>{let a,b,u;for(let k in localStorage){/\.accessToken$/.test(k)&&(a=localStorage[k]);/\.idToken$/.test(k)&&(b=localStorage[k]);/\.LastAuthUser$/.test(k)&&(u=localStorage[k]);}console.log(`ACCESS_TOKEN_LIST=${a}\nACCESS_TOKEN_DOWNLOAD=${b}\nUSER_ID=${u}`)})();
```

### Step 4 – Copy the output

The console will print something like:

```
ACCESS_TOKEN_LIST=eyJraWQiOiIzNDd2Q3lpWllCRWdJSkw3...
ACCESS_TOKEN_DOWNLOAD=eyJraWQiOiI3MEoyS3lmVHZQXC9ocUJ0...
USER_ID=123cdvf-34fd...
```

Copy **all three lines**.

### Step 5 – Create the `.env` file

Create a `.env` file (if it doesn’t exist) in the same folder as the executable and paste:

```
ACCESS_TOKEN_LIST=...
ACCESS_TOKEN_DOWNLOAD=...
USER_ID=...
```

Save the file.

### Step 6 – Check LMU path

Open `config.json` and verify the value of `lmu_base_path`.

If LMU is installed in a different location, update the path using double backslashes:

```
"D:\\Program Files (x86)\\Steam\\steamapps\\common\\Le Mans Ultimate\\UserData\\player\\Settings"
```

---

## Important Notes

- Tokens **expire**: if you receive `401 Unauthorized` errors, repeat the token steps
- **Never share** your `.env` file
- Downloads are delayed slightly to simulate human behavior(about one setup every ~2 seconds, total time ~20–30 minutes)
- Already installed setups are tracked in a database file (hymo_lmu_sm.db)
- Deleting the database file means **starting downloads from the beginning**
- To stop the program, press `CTRL + C` in the terminal

---
## ☕ Support my work
If you find this project useful and want to support its development, consider buying me a coffee!

[![](https://storage.ko-fi.com/cdn/kofi3.png?v=3)](https://ko-fi.com/seroper)

*Every coffee helps me keep the lights on and the code flowing.*

---
## JSON Configuration

The `config.json` file fully controls the downloader behavior.

## JSON Configuration

The `config.json` file fully controls the downloader behavior. 

### Logging

The logging system is divided into two separate outputs: `console` (for real-time feedback) and `file` (for persistent debugging).

| Category | Parameter | Description |
| :--- | :--- | :--- |
| **Console** | `level` | Logging level for the terminal (e.g., `INFO`, `WARNING`). |
| | `format` | Log message format for the terminal (default: `%(message)s`). |
| **File** | `level` | Logging level for the log file (usually `DEBUG` for full traceability). |
| | `format` | Detailed format including `asctime`, `name`, and `levelname`. |

### Network

Settings related to API communication with TrackTitan services.

| Parameter | Description |
| :--- | :--- |
| `base_url` | TrackTitan API base URL. |
| `consumer_id` | Client identifier for the API requests. |
| `page_size` | Number of setups to fetch per page. |
| `min_delay` | Minimum delay (seconds) between requests to avoid rate limiting. |
| `max_delay` | Maximum delay (seconds) between requests. |

### Paths

Configuration for file storage, extraction, and game directory mapping.

#### Download
| Parameter | Description |
| :--- | :--- |
| `base_path` | Folder where ZIP files are initially downloaded. |
| `clean_download_after_copy` | If `true`, deletes the ZIP files after they have been extracted and copied. |

#### Setups
| Parameter | Description |
| :--- | :--- |
| `overwrite` | If `true`, existing setup files will be overwritten. |
| `delete_previous_version` | If `true`, removes the previous version of a setup before installing the new one. |
| `lmu_base_path` | Absolute path to the Le Mans Ultimate `Settings` folder. |
| `file_extensions` | List of valid file extensions to consider as setup files (e.g., `.svm`). |

### Remote Tracks

Settings for fetching the track mapping dynamically from a remote repository.

| Parameter | Description |
| :--- | :--- |
| `enabled` | Enable or disable fetching the track map from a remote URL. |
| `url` | The direct URL to the `tracks.json` raw file. |
| `timeout` | Connection timeout in seconds for the remote request. |

### Track mapping example

```
{
  "tt_folder_name": ["Losail - WEC", "Losail"],
  "lmu_folder_name": "Qatar"
}
```

### Handling unmapped tracks

If a downloaded setup refers to a track **not listed in the JSON**, the tool will create a folder named:

```
<TRACK_NAME> - HYMO
```

This makes unmapped tracks easy to identify.

#### Adding a new track

Simply add a new entry to the `tracks` list:

```
{
  "tt_folder_name": ["My Track - WEC", "My Track"],
  "lmu_folder_name": "MyTrack"
}
```

After that, setups for this track will be copied directly into the correct LMU folder without the `- HYMO` suffix.

---

## Done

You can now run the executable and let the downloader do the work 🚀
