[33mcommit b89f5f1073f8799441566584af0c90cc805ed705[m[33m ([m[1;36mHEAD -> [m[1;32mhome[m[33m, [m[1;31morigin/home[m[33m)[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Wed Mar 28 22:21:27 2018 -0400

    Change navbar animation, styling, and bootstrap classes
    
    -Add underscore-min.js for debounce
    -Add separate scrolling and resizing functions to navbar
    -Change story_summary.html bootstrap classes
    -Rename scripts.html to head.html

[33mcommit a9ea70a2276955983a09e72e9c6f8d2d2dcd52f2[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Wed Mar 28 13:54:06 2018 -0400

    revamp index styling
    
    -remove unneeded styles
    -change custom-settings
    -custom bootstrap styles are in home.scss

[33mcommit 1e8b51c5443b86a4e5eefb011ba086b6ce0f30d0[m[33m ([m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m, [m[1;32mmaster[m[33m)[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Tue Mar 27 10:24:13 2018 -0400

    change bootstrap.html to scripts.html

[33mcommit ca5d93f0e6560fc1b9bb5275b3537c2517cf08d2[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Tue Mar 27 02:55:32 2018 -0400

    change navbar wrapper style to a lighter theme

[33mcommit dbea1715fb6613d21f32ee82f3221e1fe674bb6d[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Tue Mar 27 02:54:59 2018 -0400

    move custom settings up a directory

[33mcommit 005acc2987c32eb09de9d152fbd192218e48ffb7[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Tue Mar 27 02:54:27 2018 -0400

    change scroll animation, section styling, favicon, and custom settings
    
    -change index.js to reflect styling changes in css
    -change section to have navbar at top
    -add underscore.js to bootstrap.html

[33mcommit 164c3f9cedef8707ac2b589d45ff616c3ead9ff9[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Mon Mar 26 23:39:57 2018 -0400

    change navbar and favicon

[33mcommit 152481d0dedcfcae104813ec77c74b44619dfaa0[m
Merge: d41364a a4c3e71
Author: Mark Jung <markojungo@gmail.com>
Date:   Mon Mar 26 02:22:00 2018 -0400

    Merge branch 'master' of https://github.com/markojungo/silverchips

[33mcommit d41364a9195f92fc7177a1ceac075b2effc2c83d[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Mon Mar 26 02:21:48 2018 -0400

    change mastheads, navbar placement, and animations
    
    - change index_scroll.js to index.scroll
    - add TweenMax CDN to bootstrap.html
    - change section html to include header (rethink this design choice
    later)
    - change navbar to be sticky on section urls
    - remove doctype specifier in logo-svg.html for optimization
    - change base layout (again, rethink this code structure)
    - add absolute-top css class for index.html styling
    - make scroll button disappear on mobile
    - start logo-svg fill attribute as 'none' in css

[33mcommit a4c3e718a5ea5be815c7cedc54ad47250a7b1e0a[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Sun Mar 25 22:07:03 2018 -0400

    Update README.md

[33mcommit 3468717f369e6557e91ce520890074bb873c73f6[m
Merge: abea2de 790d954
Author: Mark Jung <markojungo@gmail.com>
Date:   Sun Mar 25 01:12:36 2018 -0400

    Merge branch 'master' of https://github.com/markojungo/silverchips

[33mcommit abea2de17317e9e0f51f124c52dc0f851dbbfaaa[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Sun Mar 25 01:12:20 2018 -0400

    Change a lot of things (read more...)
    
    - add $background-image variable to _custom-settings.scss to change
    masthead/footer background in one place
    - change mobile styling
    - add favicon to static
    - add index-masthead
    - add scroll button to index-masthead
    - navbar breakpoint is at bootstrap-xl
    - add "navbar" context to view_section in views.py in order to support
    .active style
    - add congruent_outline, dark_embroidery, and spiration dark pngs to
    test for a good background
    - add index_scroll.js which is only added to index-masthead

[33mcommit 790d954e8ce4d10613f3e70638c094f5f9f656f1[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Sun Mar 25 00:31:51 2018 -0400

    Update README.md

[33mcommit de3cfb13535387c5fc5c6abc6d10c5226b39e1cc[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Sun Mar 25 00:21:02 2018 -0400

    Update README.md

[33mcommit 9a728a52d5a457f9294620d6b3397a16d622288f[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Fri Mar 23 11:20:52 2018 -0400

    add logo-svg.html and site-index-masthead

[33mcommit 0841b3da7f27c538af41ed11056989cd55ec3c77[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Fri Mar 23 00:42:26 2018 -0400

    Add folders to home, change styles, and change footer/navbar
    
    Add images, scripts, and styles folders to static/home for organization
    Change navigation bar and footer to be slightly "cleaner"

[33mcommit e199447141cfa67859d6001dcd661e4569de45cb[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Thu Mar 22 23:35:51 2018 -0400

    update README.md

[33mcommit 20b291f67286883616b5253c2a6a9f727db61f36[m[33m ([m[1;31morigin/navbar-footer[m[33m)[m
Author: Mark Jung <markojungo@gmail.com>
Date:   Thu Mar 22 23:32:01 2018 -0400

    updated README.md

[33mcommit 3fb569f674e936adf691cf6aae8f269e53e9a58f[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Thu Jan 4 15:04:37 2018 -0500

    Removed content types from fixtures

[33mcommit f16170e1a24c5ea583777eeab337648e5aecfa8a[m
Merge: b208556 d9cbeeb
Author: Noah Kim <noahbkim@gmail.com>
Date:   Mon Jan 1 16:09:16 2018 -0500

    Merge branch 'master' of github.com:mbhs/silverchips

[33mcommit b2085568825936da2161a6979977a70beea3a35e[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Mon Jan 1 16:09:13 2018 -0500

    Creating stories works

[33mcommit d9cbeeb9a42d628bea5fb32efb4604b8f1cdecf8[m
Author: Noah Singer <singerng@gmail.com>
Date:   Mon Jan 1 16:07:53 2018 -0500

    fixed section displays

[33mcommit 73f665bcf0322caabb725631cc0ee9bab24abf52[m
Author: Noah Singer <singerng@gmail.com>
Date:   Mon Jan 1 14:19:34 2018 -0500

    display authors in story summary

[33mcommit 9f3299f100b11ee90c59e88ac9eb182706310e1f[m
Author: Noah Singer <singerng@gmail.com>
Date:   Sat Dec 23 23:13:16 2017 -0500

    sections render properly finally

[33mcommit 3e6f4bdcdbf4c3fe93f9478cd36c342634ee498c[m
Author: Noah Singer <singerng@gmail.com>
Date:   Tue Dec 19 10:38:10 2017 -0500

    updated fixtures

[33mcommit d0332c3143fa9ec5da0ac0d81b902e6308f51df6[m
Merge: 7952816 f4edf45
Author: Noah Kim <noahbkim@gmail.com>
Date:   Tue Dec 19 09:53:40 2017 -0500

    Merge branch 'master' of github.com:mbhs/silverchips

[33mcommit 79528165d9fde1b273f2f0fd296349ac7fbf05f5[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Tue Dec 19 09:53:38 2017 -0500

    Moved mixins directly into classes

[33mcommit f4edf45d870f0248e1771ccc93ec20cba52ad972[m
Author: Noah Singer <singerng@gmail.com>
Date:   Tue Dec 19 09:53:22 2017 -0500

    minor updates and upgrade to FA 5

[33mcommit 0606b0c670428498cfd91130cbe79f4389ecc4a1[m
Merge: a72e621 5a04a23
Author: Noah Singer <singerng@gmail.com>
Date:   Mon Dec 18 23:10:35 2017 -0500

    Merge branch 'master' of github.com:mbhs/silverchips

[33mcommit a72e6215fff6d8b8083c9f5aa26c194f4ed4d11f[m
Author: Noah Singer <singerng@gmail.com>
Date:   Mon Dec 18 23:10:33 2017 -0500

    updated fixtures

[33mcommit 5a04a23115ea435311b88906181b926d4cfad3db[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Sat Dec 16 13:16:03 2017 -0500

    Made the description entry a quill editor

[33mcommit fc6921fa4cec12b370f05b987028937d921101dc[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Tue Dec 12 10:30:06 2017 -0500

    Add rudimentary list view for stories

[33mcommit a9013b9b4343c41b559623d9e9a29dfbf3dea3a4[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Tue Dec 12 10:07:10 2017 -0500

    Messed with authentication

[33mcommit b62a6a2caf2f9679c5594acec92ba3b5025836a0[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Mon Dec 11 09:32:53 2017 -0500

    Added development fixtures

[33mcommit 576cda454ab1a909f9fe66b01a558bd6a4b8b6ab[m
Author: Noah Kim <noahbkim@gmail.com>
Date:   Mon Dec 11 09:18:10 2017 -0500

    Fixed up fixtures

[33m