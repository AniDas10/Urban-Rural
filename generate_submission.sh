mkdir submission_$(date +"%H-%M")
cd submission_$(date +"%H-%M")
mkdir code
mkdir data
jupyter nbconvert --to script ../learn.ipynb --output submission_$(date +"%H-%M")/code/learn
jupyter nbconvert --to script ../predict.ipynb --output submission_$(date +"%H-%M")/code/predict
cp -r ../lib code/
cp -r ../data/* data/
cp -r ../explanation.md .
cp -r ../data/results.csv .
cp -r ../data/results_country.csv .