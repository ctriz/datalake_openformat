# Use the official Bitnami Spark image
FROM bitnami/spark:3.5.0

# Set environment variables
ENV SPARK_HOME=/opt/bitnami/spark \
    PATH=$SPARK_HOME/bin:$PATH \
    PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Hudi JARs
COPY hudi-spark3.5-bundle_2.12-0.15.0.jar /opt/bitnami/spark/jars/

# Copy app source code
WORKDIR /app
COPY app/ /app/

# Build wheel and install
RUN pip install --upgrade build && \
    python -m build && \
    pip install dist/*.whl

# Use the entry point defined in your setup.py to run the application.
# To run the other script, you can override this command when running the container.
# The entry point script itself will handle the call to spark-submit.
CMD ["python", "-m", "hudi_trips_cow"]
