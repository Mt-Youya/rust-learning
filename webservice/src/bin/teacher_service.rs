#[path = "../handlers.rs"]
mod handlers;

#[path = "../routers.rs"]
mod routers;

#[path = "../state.rs"]
mod state;

#[path = "../models.rs"]
mod models;

use actix_web::{web, App, HttpServer};
use routers::*;
use state::AppState;
use std::sync::Mutex;

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    let shared_data = web::Data::new(AppState {
        health_check_response: "I'm ok".to_string(),
        visit_count: Mutex::new(0),
        courses: Mutex::new(vec![]),
    });
    let app = move || {
        App::new()
            .app_data(shared_data.clone())
            .configure(general_routes)
            .configure(course_routes)
    };
    println!("Starting server on port http://127.0.0.1:3000");
    HttpServer::new(app).bind("127.0.0.1:3000")?.run().await
}
