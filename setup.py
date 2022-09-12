from distutils.core import setup
import setup_translate


setup(name='enigma2-plugin-extensions-tmbd',
		version='6.9',
		author='Dimitrij',
		author_email='dima-73@inbox.lv',
		package_dir={'Extensions.TMBD': 'src'},
		packages=['Extensions.TMBD', 'Extensions.TMBD.tmdb3'],
		package_data={'Extensions.TMBD': ['*.png', 'ig/*.png', 'profile/*.py', 'locale/*/LC_MESSAGES/*.mo']},
		description='Search the internet bases themoviedb.org/kinopoisk.ru',
		cmdclass=setup_translate.cmdclass,
	)
