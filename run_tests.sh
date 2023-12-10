folders=$(ls -d */)

for folder in $folders
do
    cd $folder
    if [ -d "test/" ]
    then
        python -m unittest
        status_code=$?
        if [ "$status_code" == "1" ]
        then
            exit 1
        fi
        cd ../
    else
        cd ../
    fi
done