use actix_web::{error, http::StatusCode, HttpResponse, Result};
use serde::Serialize;
use sqlx::error::Error as SqlxError;
use std::fmt;
use std::fmt::{Display, Formatter};

#[derive(Debug, Serialize)]
pub enum ServiceError {
    DBError(String),
    ActixError(String),
    NotFoundError(String),
}

#[derive(Debug, Serialize)]
pub struct ServiceErrorResponse {
    error_message: String,
}

impl ServiceError {
    fn error_response(&self) -> String {
        match self {
            ServiceError::DBError(msg) => {
                println!("Database Error: {:?}", msg);
                "Database Error".into()
            }
            ServiceError::ActixError(msg) => {
                println!("Actix Error: {:?}", msg);
                "Internal server  Error".into()
            }
            ServiceError::NotFoundError(msg) => {
                println!("Not Found Error: {:?}", msg);
                msg.into()
            }
        }
    }
}


impl error::ResponseError for ServiceError  {
    fn status_code(&self) -> StatusCode {
        match self {
            ServiceError::DBError(msg) | ServiceError::ActixError(msg) => {
                StatusCode::INTERNAL_SERVER_ERROR
            }
            ServiceError::NotFoundError(_) => StatusCode::NOT_FOUND,
        }
    }
    fn error_response(&self) -> HttpResponse {
        HttpResponse::build(self.status_code()).json(ServiceErrorResponse {
            error_message: self.error_response(),
        })
    }
}

impl From<actix_web::error::Error> for ServiceError {
    fn from(err: actix_web::error::Error) -> Self {
        ServiceError::ActixError(err.to_string())
    }
}

impl Display for ServiceError {
    fn fmt(&self, f: &mut  Formatter) -> Result<(), fmt::Error> {
        write!(f, "{}", self)
    }
}
impl From<SqlxError> for ServiceError {
    fn from(err: SqlxError) -> Self {
        ServiceError::DBError(err.to_string())
    }
}
