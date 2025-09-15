# Solirium - Hedera Africa Hackathon Project

## Overview

Solirium is a decentralized physical infrastructure (DePIN) network for micro-leasing and fractional ownership of solar panels built on the Hedera blockchain. The project enables tokenization of solar panels through NFTs and facilitates sharing of energy generation data through IoT sensor simulation. The system creates a bridge between physical solar infrastructure and blockchain technology, allowing for transparent tracking and ownership of renewable energy assets.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask Web Application**: Chosen for its simplicity and rapid development capabilities. Flask provides the core web server functionality and API endpoints for the solar panel management system.

### Blockchain Integration
- **Hedera Network Integration**: Uses the hiero-sdk-python library to interact with Hedera's consensus service and token service. The system creates non-fungible tokens (NFTs) to represent individual solar panels, enabling fractional ownership and transparent asset management.
- **Token Management**: Implements NFT creation for solar panels with configurable supply limits. Each solar panel is represented as a unique NFT with metadata including name, symbol, and operational parameters.
- **Account Management**: Configured with operator accounts and private keys for transaction signing and network communication.

### IoT Simulation Layer
- **Sensor Data Simulation**: Implements realistic solar panel performance simulation based on time-of-day patterns. The system generates mock sensor data including energy output (Wh), voltage, and temperature readings.
- **Data Collection**: Simulates continuous data streams from solar panels with configurable intervals, mimicking real-world IoT sensor behavior.

### Configuration Management
- **Environment-Based Configuration**: Uses python-dotenv for managing sensitive credentials and network configurations. Supports both testnet and mainnet Hedera network deployments.
- **Flexible Network Selection**: Architecture allows switching between different Hedera network environments through environment variables.

### Data Architecture
- **In-Memory Storage**: Current implementation uses global variables for panel data storage, suitable for proof-of-concept and development phases.
- **Real-time Data Processing**: Implements threading for continuous sensor data simulation while maintaining web server responsiveness.

## External Dependencies

### Blockchain Services
- **Hedera Network**: Primary blockchain infrastructure for token creation, NFT minting, and transaction processing
- **hiero-sdk-python (v0.1.4)**: Official Python SDK for Hedera blockchain interactions

### Web Framework
- **Flask (v3.1.2)**: Web application framework for API endpoints and server functionality

### Utility Libraries
- **python-dotenv (v1.0.1)**: Environment variable management for secure credential handling
- **requests (v2.32.3)**: HTTP client library for external API communications

### Development Environment
- **Python 3.7+**: Runtime environment requirement for all application components