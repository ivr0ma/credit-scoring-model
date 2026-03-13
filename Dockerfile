FROM treeverse/lakefs:latest

# Simple helper image to use lakectl client inside a container
ENTRYPOINT ["lakectl"]
CMD ["--help"]

