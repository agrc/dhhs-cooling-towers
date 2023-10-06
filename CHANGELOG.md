# Changelog

## 1.0.0 (2023-10-06)


### 🚀 Features

* add more error info ([e0c092b](https://github.com/agrc/dhhs-cooling-towers/commit/e0c092b63d1b32324f3e4be761a6b3f5334cfea0))
* add more perf_counters ([96ffc34](https://github.com/agrc/dhhs-cooling-towers/commit/96ffc342467653c4f7f04dc88e62527c32121fae))
* add script to build WMTS index ([59252f4](https://github.com/agrc/dhhs-cooling-towers/commit/59252f442e6559ad8cec9ae4a101865d7c0de95a))
* add skip/take to logs ([aebb49d](https://github.com/agrc/dhhs-cooling-towers/commit/aebb49d2db65d42bac377969172d114c734cfbde))
* adjust conf and overlap thresholds for more towers ([d19a6cd](https://github.com/agrc/dhhs-cooling-towers/commit/d19a6cd1cd5b6cd0f2c93d3adb5a0e218cea16f1))
* append results into big query ([8c7a63c](https://github.com/agrc/dhhs-cooling-towers/commit/8c7a63c75c06d02cef2184e2c97b818e83b3b9b6))
* check status, only call update_index on success ([d586afc](https://github.com/agrc/dhhs-cooling-towers/commit/d586afc5046bd06b975a5c35de1e47c2f6de396d))
* defend bq table edits ([e38c426](https://github.com/agrc/dhhs-cooling-towers/commit/e38c426428216f2369485491db02a0dd3701f2ee))
* function to process all tiles ([037de59](https://github.com/agrc/dhhs-cooling-towers/commit/037de59066a905d508dcf85bc2f58687eaea4b2b))
* function to update bq index ([cd6cab4](https://github.com/agrc/dhhs-cooling-towers/commit/cd6cab4e0d09e869eec6870568b2d93e054a0225))
* get defensive with the model ([eeac863](https://github.com/agrc/dhhs-cooling-towers/commit/eeac86325b6284de87fe69d6eca6884403df24ae))
* get rows from bigquery function ([f9cd35d](https://github.com/agrc/dhhs-cooling-towers/commit/f9cd35dcc4a577735e1ef317f3543e21d0689ee7))
* initial code push ([#1](https://github.com/agrc/dhhs-cooling-towers/issues/1)) ([4390710](https://github.com/agrc/dhhs-cooling-towers/commit/4390710d08e32df9a06a5605b76dcdb27b1baa16))
* main function for cloud run ([aa67381](https://github.com/agrc/dhhs-cooling-towers/commit/aa67381be101aee6e46a8d71d9bda76def1ed55b))
* play some defense on mercantile ([b1c2228](https://github.com/agrc/dhhs-cooling-towers/commit/b1c2228b5e6be74ce9b39278b3244f13e8f0eb9e))
* print sorted results in CLI ([40c184b](https://github.com/agrc/dhhs-cooling-towers/commit/40c184b9c8dec83d53a59df07c7914b663bac535))
* set insert method with chunksize for results ([19e2536](https://github.com/agrc/dhhs-cooling-towers/commit/19e2536d5bcc3e5c0289f65db579ec92ceaeb31b))
* skip/take from env variables ([3006512](https://github.com/agrc/dhhs-cooling-towers/commit/30065128ba6721d33fbb4622538aea6cc8f138cd))


### 🐛 Bug Fixes

* all code paths should have a return ([8e15052](https://github.com/agrc/dhhs-cooling-towers/commit/8e150521cfe0c16473c7a8865f650a7cc465a2be))
* assign variables before using ([11d8345](https://github.com/agrc/dhhs-cooling-towers/commit/11d8345dfb62d87d7ff556e351762d08a6b15818))
* import environ ([79ff36a](https://github.com/agrc/dhhs-cooling-towers/commit/79ff36a127e29919bca5113fc8300132706594ce))
* naming conventions ([ab7b398](https://github.com/agrc/dhhs-cooling-towers/commit/ab7b398af4dd8c2c314e59f361b06b9a228b0e6b))
* only append tiles that are not None ([c082230](https://github.com/agrc/dhhs-cooling-towers/commit/c082230fe15b84820a3af29e2794cc3ce5cf1447))
* perf_counter on downloads ([942adce](https://github.com/agrc/dhhs-cooling-towers/commit/942adce29e9bf9b8390bcce1edf7e591aae3fa96))
* reduce offset size to improve query performance ([d058c4f](https://github.com/agrc/dhhs-cooling-towers/commit/d058c4f20237ad6fa1247a416cf85cd796a9b4f1))
* requirements ([1f6f17b](https://github.com/agrc/dhhs-cooling-towers/commit/1f6f17ba1ad2922b9d1ae8778105d317def03025))
* update connector creation ([3460901](https://github.com/agrc/dhhs-cooling-towers/commit/34609013f5b3b5b8eb9d9b446397a1ae0badcba9))
* update index if no results ([b3213e5](https://github.com/agrc/dhhs-cooling-towers/commit/b3213e5cf95a9e7c822fad115e3d5d1139b97d00))
* update logging ([3c7d704](https://github.com/agrc/dhhs-cooling-towers/commit/3c7d704db12f1a0f922e0b46c4f73eda213db4a7))


### 📖 Documentation Improvements

* add cooling tower ID references to readme ([3a22782](https://github.com/agrc/dhhs-cooling-towers/commit/3a227827e12e01f700c60108deabbd2a562e2e24))
* add directory info ([db78bf4](https://github.com/agrc/dhhs-cooling-towers/commit/db78bf4d9faf9a098a813242081e0325d66e83b7))
* add how to run the batch job ([293bdf2](https://github.com/agrc/dhhs-cooling-towers/commit/293bdf228c538e2165a24f6c2c02c8c0dbf332d0))
* add index creation ([e37f40b](https://github.com/agrc/dhhs-cooling-towers/commit/e37f40b931311d4e6c832bcb4393d2efba1efc09))
* add small batch cloud run values ([e9bb75b](https://github.com/agrc/dhhs-cooling-towers/commit/e9bb75b817977367710c3b67b32752cb6a629540))
* add some CLI info ([79c567b](https://github.com/agrc/dhhs-cooling-towers/commit/79c567bdabac260cb83aa3b9d57de871909825a6))
* clean up docstring and comments ([7bb8e00](https://github.com/agrc/dhhs-cooling-towers/commit/7bb8e008ec3256fee1af7fc072c2ad9449fb9719))
* document how to prepare the data ([66c51c1](https://github.com/agrc/dhhs-cooling-towers/commit/66c51c15e9b9c3ca4e3cd09724bd44ac02ffa1ef))
* fix copy paste error ([6dd3b4e](https://github.com/agrc/dhhs-cooling-towers/commit/6dd3b4e9723866d987549a15bd312a9ac022ac88))
* grammar ([a664cdb](https://github.com/agrc/dhhs-cooling-towers/commit/a664cdb138d1762dad1c18455f938cc665bee981))
* must grant access to users ([187741a](https://github.com/agrc/dhhs-cooling-towers/commit/187741a534166528c38ddf7c0204a0eb54e2b266))
* remove unnecessary steps ([2b70962](https://github.com/agrc/dhhs-cooling-towers/commit/2b7096210b5698fa16cf1216979c2c15c0dd398e))
* reorder data prep steps ([eb95a54](https://github.com/agrc/dhhs-cooling-towers/commit/eb95a54469fbaf41b4f8bdd362487f2a38e57243))
* update readme with prerequisites ([fd7f679](https://github.com/agrc/dhhs-cooling-towers/commit/fd7f67934661b40c642e2681bacbd57d59347fa1))


### 🎨 Design Improvements

* change to getenv import ([c4e6e07](https://github.com/agrc/dhhs-cooling-towers/commit/c4e6e0769047a7fcebfea0f35840c34b343e171f))
* formatting ([90111e0](https://github.com/agrc/dhhs-cooling-towers/commit/90111e054df17edcd421e4fd7acd6fc804c24b50))
* formatting ([fa4ed17](https://github.com/agrc/dhhs-cooling-towers/commit/fa4ed1725b06f94fcc80bc5ecc7610316ac721b6))
* formatting ([0d9731f](https://github.com/agrc/dhhs-cooling-towers/commit/0d9731fd74a0a6ea57e7e407b623e48a8f83d29a))
* remove unnecessary else ([4c7978e](https://github.com/agrc/dhhs-cooling-towers/commit/4c7978e84fa4bde317b9b09509d9a1531eafe360))
* remove unnecessary returns ([f795f57](https://github.com/agrc/dhhs-cooling-towers/commit/f795f57c852b768f22159b6a3281cfe9d74ab6da))
* trim extra spaces ([7fed109](https://github.com/agrc/dhhs-cooling-towers/commit/7fed10951535d61c346990d277ca3effc7c60905))
* trim whitespace and extra newlines ([726fc37](https://github.com/agrc/dhhs-cooling-towers/commit/726fc37ddb0088ca06af924f1297d29a18b059c2))
* use getenv ([c95ea95](https://github.com/agrc/dhhs-cooling-towers/commit/c95ea9545bab36a0279c25380c291bbf22a3e11b))

## [1.0.0-6](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-5...v1.0.0-6) (2023-05-17)


### 🐛 Bug Fixes

* reduce offset size to improve query performance ([d8b27a7](https://github.com/agrc/dhhs-cooling-towers/commit/d8b27a783a754f7878431c23bf12ee969f130578))

## [1.0.0-5](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-4...v1.0.0-5) (2023-05-17)


### 🐛 Bug Fixes

* update logging ([dbfa5bc](https://github.com/agrc/dhhs-cooling-towers/commit/dbfa5bc0c54d23693165c8d89262420ecf50f2b2))


### 📖 Documentation Improvements

* add index creation ([c24840d](https://github.com/agrc/dhhs-cooling-towers/commit/c24840d6af1ad64f55d653318b342ab650d809d8))


### 🚀 Features

* set insert method with chunksize for results ([60b448b](https://github.com/agrc/dhhs-cooling-towers/commit/60b448bb4e15e48adc1ef4f5ec6f4616ea1f11e8))

## [1.0.0-4](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-3...v1.0.0-4) (2023-05-16)


### 📖 Documentation Improvements

* must grant access to users ([d835867](https://github.com/agrc/dhhs-cooling-towers/commit/d835867ea606c4fdf1919f6ddca7335a9bc95579))

## [1.0.0-3](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-2...v1.0.0-3) (2023-05-16)


### 📖 Documentation Improvements

* reorder data prep steps ([05d951e](https://github.com/agrc/dhhs-cooling-towers/commit/05d951e08c1d3f3de05bde065b151a70845a4abf))


### 🐛 Bug Fixes

* update connector creation ([78f22c2](https://github.com/agrc/dhhs-cooling-towers/commit/78f22c21316e8becb88679d96cd3bee20057cc83))

## [1.0.0-2](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-1...v1.0.0-2) (2023-05-16)


### 📖 Documentation Improvements

* add how to run the batch job ([6856009](https://github.com/agrc/dhhs-cooling-towers/commit/68560099e9b831a06a0998444307cfb7d4bb2d71))
* document how to prepare the data ([bf9afe8](https://github.com/agrc/dhhs-cooling-towers/commit/bf9afe88e9b39925557258667ce06c3ce9e62337))
* grammar ([80709a9](https://github.com/agrc/dhhs-cooling-towers/commit/80709a977a6ce97e77f83939daa8ddebbd47dff1))
* remove unnecessary steps ([7a255ed](https://github.com/agrc/dhhs-cooling-towers/commit/7a255edbd139d396ecf70a002a32dceca2ebcf4f))


### 🎨 Design Improvements

* formatting ([be58bed](https://github.com/agrc/dhhs-cooling-towers/commit/be58bed234ae9546b76340112083a0b38ed127f6))

## [1.0.0-1](https://github.com/agrc/dhhs-cooling-towers/compare/v1.0.0-0...v1.0.0-1) (2023-05-15)


### 📖 Documentation Improvements

* add small batch cloud run values ([5afbc6a](https://github.com/agrc/dhhs-cooling-towers/commit/5afbc6a6e960d2f47a3242f9a627459cd84c806f))


### 🚀 Features

* add skip/take to logs ([b65faad](https://github.com/agrc/dhhs-cooling-towers/commit/b65faad4e5f8e5b9e4109cf19abea3b597326206))


### 🐛 Bug Fixes

* update index if no results ([a35009a](https://github.com/agrc/dhhs-cooling-towers/commit/a35009a89569fde21d86527e40aa1ac4b7c3a5a4))

## 1.0.0-0 (2023-05-15)


### 🎨 Design Improvements

* change to getenv import ([2c7acf8](https://github.com/agrc/dhhs-cooling-towers/commit/2c7acf80ef19f11dc080f29415236db808a4dd0b))
* formatting ([30e5344](https://github.com/agrc/dhhs-cooling-towers/commit/30e53442f4f3e73bdb50b70ddc597d6cd40a33eb))
* formatting ([de47d93](https://github.com/agrc/dhhs-cooling-towers/commit/de47d93250b0533a961a23447726d07ee12e51a5))
* remove unnecessary else ([18d22d0](https://github.com/agrc/dhhs-cooling-towers/commit/18d22d096209206760b0ee559ba0f692540c0d10))
* remove unnecessary returns ([d7909e2](https://github.com/agrc/dhhs-cooling-towers/commit/d7909e246a083dcfd95cc0a4d856ef8bc3e9ed09))
* trim extra spaces ([afc9368](https://github.com/agrc/dhhs-cooling-towers/commit/afc9368d17ee16f1f8eaa4a2918d0d9969e19644))
* trim whitespace and extra newlines ([469aec3](https://github.com/agrc/dhhs-cooling-towers/commit/469aec3841a88ab58f40051025a463329a2062c5))
* use getenv ([2951568](https://github.com/agrc/dhhs-cooling-towers/commit/29515685722322d3f917fc499b0cc766b4680860))


### 📖 Documentation Improvements

* add directory info ([8e7b79e](https://github.com/agrc/dhhs-cooling-towers/commit/8e7b79e8c8f1787eec88735db7452f5bb94b6aee))
* add some CLI info ([953144c](https://github.com/agrc/dhhs-cooling-towers/commit/953144c8ddaef150d6307b88619e6a9d01cac8b8))
* clean up docstring and comments ([18f0657](https://github.com/agrc/dhhs-cooling-towers/commit/18f0657ad03a5ff55807d71d7fce7a5533933793))
* fix copy paste error ([f77ec07](https://github.com/agrc/dhhs-cooling-towers/commit/f77ec07fd58cd00ef2f06b43882ff18737a8e4c5))


### 🚀 Features

* add more error info ([b03e55f](https://github.com/agrc/dhhs-cooling-towers/commit/b03e55fae7763441d13806f21f2fe1eeb3fc8b41))
* add more perf_counters ([b0f2975](https://github.com/agrc/dhhs-cooling-towers/commit/b0f2975f755ce794edd0623425226eab313bd089))
* adjust conf and overlap thresholds for more towers ([30217b5](https://github.com/agrc/dhhs-cooling-towers/commit/30217b5b0262ce5a102181c636cedb769c592136))
* append results into big query ([d89e073](https://github.com/agrc/dhhs-cooling-towers/commit/d89e0733bac7c397a8cd9dccd15980eed38c1506))
* check status, only call update_index on success ([a130475](https://github.com/agrc/dhhs-cooling-towers/commit/a1304754eaa87807c9aa63b3388e6497d40d47b3))
* defend bq table edits ([ece2e43](https://github.com/agrc/dhhs-cooling-towers/commit/ece2e43fc1301b1227aa5c81dc64df4a40e7a8a2))
* function to process all tiles ([a8596c6](https://github.com/agrc/dhhs-cooling-towers/commit/a8596c648fa44d909a2c4c02d0abe91373ec8844))
* function to update bq index ([596dc05](https://github.com/agrc/dhhs-cooling-towers/commit/596dc051b9143531ea03fdbf10a267f7d19eec8f))
* get defensive with the model ([9cd4b3c](https://github.com/agrc/dhhs-cooling-towers/commit/9cd4b3ccd39b9edc71c855446648c6278b293701))
* get rows from bigquery function ([72b1ca3](https://github.com/agrc/dhhs-cooling-towers/commit/72b1ca3d451bf4ff8778da147af8f583585c6dda))
* initial code push ([#1](https://github.com/agrc/dhhs-cooling-towers/issues/1)) ([009a05c](https://github.com/agrc/dhhs-cooling-towers/commit/009a05ce7f3d071d2befa4b49613f49487c3b907))
* main function for cloud run ([7ed70f5](https://github.com/agrc/dhhs-cooling-towers/commit/7ed70f5948ac2141deb18f3544362bd39c46eb76))
* play some defense on mercantile ([3968a97](https://github.com/agrc/dhhs-cooling-towers/commit/3968a978330d2530b7e29b0433f03f9e01f46df7))
* print sorted results in CLI ([41e6a01](https://github.com/agrc/dhhs-cooling-towers/commit/41e6a01204c1d52cfa6653c45dd9d564f87cd0d8))
* skip/take from env variables ([1242105](https://github.com/agrc/dhhs-cooling-towers/commit/1242105836b85c04196f965d2731cafde841e9ad))


### 🐛 Bug Fixes

* all code paths should have a return ([a316a5d](https://github.com/agrc/dhhs-cooling-towers/commit/a316a5df53f5f789a95f773f47e797c936a21256))
* assign variables before using ([2710887](https://github.com/agrc/dhhs-cooling-towers/commit/2710887980297de3fceb364188c2faa8c5d6103b))
* import environ ([7469b18](https://github.com/agrc/dhhs-cooling-towers/commit/7469b1825dda979e08fce04b537b31ffbcb161b8))
* naming conventions ([dea8049](https://github.com/agrc/dhhs-cooling-towers/commit/dea8049e9f96501caae70bb733a0f2d74fcb437d))
* only append tiles that are not None ([487bf8e](https://github.com/agrc/dhhs-cooling-towers/commit/487bf8e58fd7c282bbe80e19108b0eee5fb2cd89))
* perf_counter on downloads ([6b393c0](https://github.com/agrc/dhhs-cooling-towers/commit/6b393c09348db8ff309164206fb007ecab729e2b))
* requirements ([93dd3aa](https://github.com/agrc/dhhs-cooling-towers/commit/93dd3aa863c30224d152bfc271d8883a77ddd555))
