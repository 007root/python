dir=$(dirname $(readlink -f "$0"))

echo 'Config vundle...'
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

if [[ -e ~/.vimrc ]]; then
    cp ~/.vimrc{,.bak}
    echo -e "\033[32mBackup local .vimrc to ~/.vimrc.bak\033[0m"
fi

cp -f $dir/{.vimrc,.pylintrc} ~/

echo 'Config vimrc...'
pip install pylint 2>&1 > /dev/null &
vim +PluginInstall +qall 2>&1 > /dev/null
echo 'Finished...'
