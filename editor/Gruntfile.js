module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    browserify: {
      dist: {
        options: {
          transform: [
            ["babelify",
              {"presets": ['es2015']}
            ]
          ],
          extensions: ['js']
        },
        files: {
          ".tmp/bundle.js": ["public/js/main.js"]
        }
      }
    },
    clean: {
      dist: [".tmp"],
      options: { "verbose": true }
    }
  });

  // grunt.loadNpmTasks('grunt-browserify');
  // grunt.loadNpmTasks('grunt-contrib-clean');

  grunt.registerTask('build', ['clean', 'browserify']);
}
