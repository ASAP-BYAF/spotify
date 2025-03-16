from main import main

def handler(event, lambda_context):
    main()
    

if __name__ == "__main__":
    handler(None, None)