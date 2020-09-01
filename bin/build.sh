source ~/.bash_profile
bdc build.yaml -o
cp ~/tmp/curriculum/ml-scale-1.0.0/StudentFiles/Labs.dbc .
databricks workspace delete /Users/$USER@databricks.com/ml-scale -r
databricks workspace import Labs.dbc /Users/$USER@databricks.com/ml-scale -f DBC -l PYTHON
rm Labs.dbc
