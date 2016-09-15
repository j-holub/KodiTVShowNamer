# Kodi TV Show Namer

This is a small Python script to rename TV show episodes in a way, that the [Kodi](https://kodi.tv) scraper will correctly parse the information.

The episodes will be in the following format (assuming that the original file was an mkv).

```
showname.epXX.YEAR.mkv
```
or if the season should be included

```
showname.sX.eXX.YEAR.mkv
```

This script will also rename subtitle files of the types `srt`, `ass`, `sub` and `idx` and a language suffix can be added.



## Install

Clone the repository.

```
git clone https://github.com/00SteinsGate00/KodiTVShowNamer.git
```

To install the script, just copy it to `/usr/bin` and give it the correct permissions.

From inside the repository's directory run

```
sudo cp KodiTVShowNamer.py /usr/bin/koditvshownamer
sudo chmod +x /usr/bin/koditvshownamer
```


## Usage

The basic usage is

```
koditvshownamer <directory> <tvshow name>
```

This will check all files inside `<directory>` and rename them into `<tvshow name>.epXX.mkv`.

To determine the episode number the files are checked for the pattern `epXX`. A different Regular Expression can be specified.


### Options

| Option | Alternative | Effect | Discription |
| ------ | ----------- | ------ | ----------- |
| `-r`   | `--regex`   | RegEx  | Specifies the regular expression to find the episode number in the original file |
| `-y`   | `--year`    | Year   | The year the tv show was released |
| `-s`   | `--season`  | Season | The season number |
| `-su`  | `--subitle` | Subtitle language | To add a language suffix to the subitlte files |

You can also display the possible parameters using

```
koditvshownamer --help
```

### Regular Expression for Finding the Episode Number

Since your TV show files can have any arbitray way the episode numbers are formatted, you can specify a regular expression to match them.

Here you find some basic ones, that occur quite often

| RegEx | Description | Example |
| ----- | ----------- | ------- |
| `e[0-2][0-9]` | Starting with e and followed by 2 numbers | showA_e12.mkv |
| `- ep[0-2][0-9] -` | Episode titles are enclosed by `-` | showA - ep22 - title.mkv |
| `台[0-2][0-9]話` | Basically the way Japanese episodes are numbered | 番組A第２話.mkv |

Given those examples it should easy to build the ones you need. Here you can find some useful information on how to construct the fitting regular expressions: [regexr.com](http://regexr.com).


## Examples

Here you can find some examples on how to use this script. Once you got the hang of it, it's really simple to use but saves you a lot of time.

### Basic

```
koditvshownamer . "SteinsGate" -y 2010
```
Episodes will have the form `SteinsGate.epXX.2010.mkv`

### With RegEx


```
koditvshownamer . "Battlestar Galactica" -s 1 -r "E[0-2][0-9]"
```
Episodes will have the form `Battlestar Galactica.s1.eXX.mkv`. Here a Regular Expression was used to determine episode numbers. The original files could have looked something like `bsg E12.mkv`.

### With Subtitles

```
koditvshownamer . "太陽の歌" -r "台[0-1][0-9]話" -su en
```

This will result in video files in the form `太陽の歌.epXX.mkv` and the subtitle files will have the language suffix attached: `太陽の歌.epXX.en.srt`.


## Licence

[MIT Licence](LICENCE.md)