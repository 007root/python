set nocompatible            " required
filetype off                " required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()         " required

Plugin 'gmarik/Vundle.vim'

Plugin 'w0rp/ale'
let b:ale_linters = {
\   'python': ['pylint'],
\}
let g:ale_sign_column_always = 1
let g:ale_sign_error = 'E'
let g:ale_sign_warning = 'W'

highlight clear ALEErrorSign
highlight clear ALEWarningSign

call vundle#end()           " required
filetype plugin indent on   " required

syntax on
:set encoding=utf-8
:set tabstop=4
:set shiftwidth=4
:set expandtab
:set softtabstop=4
:set fileencoding=utf-8
