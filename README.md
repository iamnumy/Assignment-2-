# Assignment-2-
Assignment 2 (DL 10.03)


## Overview

This project implements a distributed client-server system using XML-RPC in Python. The system serves as a digital notebook, allowing users to add, retrieve, and manage notes. It also integrates with the Wikipedia API to fetch and append information to notes based on user queries.

## Features

- Add and retrieve notes with topics and timestamps.
- Append data from Wikipedia to existing notes.
- Handle multiple client requests concurrently.
- Basic error handling and logging.

## System Requirements

- Python 3.x
- `xmlrpc.client` and `xmlrpc.server` for RPC communication.
- `requests` library for Wikipedia API integration.
- Internet connection for Wikipedia API access.

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
