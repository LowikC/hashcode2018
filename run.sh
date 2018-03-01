
## declare an array variable
declare -a arr=("inputs/a_example.in" "inputs/b_should_be_easy.in" "inputs/")

## now loop through the above array
for i in "${arr[@]}"
do
   echo "$i"
   # or do whatever with individual element of the array
done