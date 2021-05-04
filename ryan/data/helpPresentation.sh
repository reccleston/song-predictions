if [ $# != 2 ]; then
    echo "Usage: [input html] [output html]";
fi
sed 's:reveal.js/://cdn.jsdelivr.net/reveal.js/2.6.2/:g' $1 > $2