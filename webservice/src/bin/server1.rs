use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use std::io;

pub fn general_routes(cfg: &mut web::ServiceConfig) {
    cfg.route("/health", web::get().to(health_check_handler));
}

// 配置 handler
pub async fn health_check_handler() -> impl Responder {
    HttpResponse::Ok().json("Actix Webservice is starting!")
}

// 实例化 HTTP server 并运行
#[actix_rt::main]
async fn main() -> io::Result<()> {
    let app = move || App::new().configure(general_routes);
    HttpServer::new(app).bind(("127.0.0.1", 3000))?.run().await
}
// cargo run -p webservice --bin server1
// cd webservice && cargo run --bin server1
