# bigData


# Installation
1. Clone the repository:
```bash
git clone https://github.com/Samerhajj/bigData.git
```
2. change directory:
```bash
cd bigData
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

# Usage

- Run the script
    - Open a command-line interface.
    - Navigate to the repository directory.
    - Execute the following command:
```bash
python main.py path/to/excel_file.xlsx
```

# Hadoop

# Running
1. Make sure hadoop is running, 
```bash
start-all.sh
```
2. Edit runhadoop file to match your streaming jar location and all the files required in hdfs/mapper/reducer
3. After Hadoop is running and configured runhadoop you can run 
```bash
./runhadoop
```
