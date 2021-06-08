FROM continuumio/miniconda3

# Install the conda environment
COPY map1.geojson /
COPY app.py /
COPY entities.txt /
RUN conda env update --name base --file environment.yml && conda clean -a

# Add conda installation dir to PATH (instead of doing 'conda activate')
ENV PATH /opt/conda/bin:$PATH

# Dump the details of the installed packages to a file for posterity
RUN conda env export --name base > base.yml

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
