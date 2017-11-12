Extend benchmark test case
==============================================================================

First, let's take a look at ``run.py`` file (``/compress-project/benchmark/run.py``), this is how a test case looks like:

.. code-block:: python

    class C1_Alice29(Case):  # inherit from Case
        # describe your test case, data type, size, etc ...
        description = "http://corpus.canterbury.ac.nz/descriptions/cantrbry/text.html"

        # a method setup your test files, typically you can download it from somewhere
        def setup(self):
            file_path = self.dirpath.append_parts(
                "alice29.txt")  # define the file path
            if not file_path.exists():
                # define where to download the file
                url = "https://s3.amazonaws.com/www.wbh-doc.com/FileHost/compress-project-test-data/alice29.txt"
                # get content
                content = spider.get_content(url)
                # write to file
                file_path.write_bytes(content)

        def run_benchmark(self):  # this method helps you to customize you test case
            # for exmaple, it's a 140KB file, we can run this 10 times
            # for large test case, I recommend smaller number
            return self._run_benchmark(repeat_times=10)

So you can easily define your own test case, and remove useless test case from the code. And then:

.. code-block:: bash

    make benchmark