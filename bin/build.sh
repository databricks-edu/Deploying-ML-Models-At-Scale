source ~/.bash_profile
bdc build.yaml -o
cp ~/tmp/curriculum/ml-deploy-1.0.0/StudentFiles/Labs.dbc .
databricks workspace delete /Users/$USER@databricks.com/ml-deploy -r
databricks workspace import Labs.dbc /Users/$USER@databricks.com/ml-deploy -f DBC -l PYTHON
rm Labs.dbc
