# GAIA Windows Container

Docker container for [AMD GAIA](https://github.com/amd/gaia) - Windows edition.

## Status: Planned Feature

The Windows container variant is currently planned for future development. This container will provide AMD GAIA in a Windows-based Docker environment.

## Expected Features (Subject to Change)

- Windows Server Core or Nano Server base
- AMD GAIA installed from PyPI
- PowerShell environment
- Similar configuration to gaia-linux with Windows-specific adaptations

## Timeline

This feature is currently in the planning phase. Check the [GitHub repository](https://github.com/itomek/gaia-docker) for updates on development progress.

## Alternatives

While the Windows container is in development, you can use:

- **[gaia-linux](../gaia-linux/README.md)** - Runtime container (works with Docker Desktop on Windows)
- **[gaia-dev](../gaia-dev/README.md)** - Development container (works with Docker Desktop on Windows)

Both Linux containers can run on Windows using Docker Desktop with WSL2 backend.

## Contributing

Interested in helping develop the Windows container? Check out the [contribution guidelines](https://github.com/itomek/gaia-docker/blob/main/CONTRIBUTING.md) or open an issue to discuss.

## Support

- **Feature Requests**: https://github.com/itomek/gaia-docker/issues
- **GAIA Issues**: https://github.com/amd/gaia/issues

## License

MIT License - see [LICENSE](../../LICENSE) file
