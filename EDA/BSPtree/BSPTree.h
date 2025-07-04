#ifndef BSPTREE_H
#define BSPTREE_H

#include <memory>
#include <vector>
#include <functional>
#include "Plane.h"
#include "Ball.h"

#if __cplusplus < 201402L
namespace std {
    template<typename T, typename... Args>
    unique_ptr<T> make_unique(Args&&... args) {
        return unique_ptr<T>(new T(std::forward<Args>(args)...));
    }
}
#endif
// Forward declarations
template <typename T>
class BSPNode;

template <typename T>
class BSPTree;

// BSPNode class template
template <typename T = NType>
class BSPNode {
private:
    Plane<T> partition_;
    std::unique_ptr<BSPNode<T>> front_;
    std::unique_ptr<BSPNode<T>> back_;
    std::vector<Polygon<T>> polygons_;

public:
    BSPNode() : partition_(), front_(nullptr), back_(nullptr) {}
    ~BSPNode() = default;

    BSPNode(const BSPNode&) = delete;
    BSPNode& operator=(const BSPNode&) = delete;

    // Getters
    const Plane<T>& getPartition() const { return partition_; }
    const std::vector<Polygon<T>>& getPolygons() const { return polygons_; }
    const BSPNode<T>* getFront() const { return front_.get(); }
    const BSPNode<T>*  getBack() const { return  back_.get(); }

    void insert(const Polygon<T>& polygon) {
        // base
        if (polygons_.empty()) {
            polygons_.push_back(polygon);
            partition_ = polygon.getPlane();
            front_ = nullptr;
            back_ = nullptr;
            return;
        }

        RelationType sit = polygon.relationWithPlane(partition_);
        // std::cout << sit << std::endl;
        // recursive
        if (sit == IN_FRONT) {
            if (front_.get() == nullptr) {
                front_ = std::make_unique<BSPNode<T>>();
            }
            front_->insert(polygon);
            return;
        } else if (sit == BEHIND) {
            if (back_.get() == nullptr) {
                back_ = std::make_unique<BSPNode<T>>();

            }
            back_->insert(polygon);
            return;
        } else if (sit == COINCIDENT) {
            polygons_.push_back(polygon);
            return;
        } else {
            auto [back, front] = polygon.split(partition_);
            // std::cout  << back << front << std::endl;
            if (front_.get() == nullptr) {
                front_ = std::make_unique<BSPNode<T>>();
            }
            if (back_.get() == nullptr) {
                back_ = std::make_unique<BSPNode<T>>();
            }
            // insert both sides
            front_->insert(front);
            back_->insert(back);
            return;
        }

    }

    // Método de consulta: recolecta en 'results' los polígonos que pueden colisionar con la Ball.
    void query(const Ball<T>& ball, const LineSegment<T>& movement, std::vector<Polygon<T>>& results) const {
       auto d0 = partition_.distance(movement.getP1());
       auto d1 = partition_.distance(movement.getP2());
       auto r = ball.getRadius();
       // both point in the same side of the plane
       if (d0 > r && d1 > r) {
           if (front_)
               front_->query(ball, movement, results);
           return;
       }
       if (d0 < -r && d1 < -r) {
           if (back_)
               back_->query(ball, movement, results);
           return;
       }
       // radius invadeo other side
       for (auto it: polygons_) {
           //std::cout << it<< std:: endl;
           results.push_back(it);
       }
       // search both sides
       if (front_)
           front_->query(ball, movement, results);
       if (back_)
           back_->query(ball, movement, results);
    }
    
    // Print
    void print(std::ostream& os, int indent = 0) const{
        std::string indentStr(indent * 4, ' ');
        
        os << indentStr << "BSPNode:\n";
        os << indentStr << "  Partition: " << partition_ << "\n";
        
        // Imprimir  polígonos
        os << indentStr << "  Polygons (" << polygons_.size() << "): ";
        if (polygons_.empty()) {
            os << "None\n";
        } else {
            os << "\n";
            for (size_t i = 0; i < polygons_.size(); ++i) {
                os << indentStr << "    [" << i << "]: " << polygons_[i] << "\n";
            }
        }
        
        // Front
        if (front_) {
            os << indentStr << "  Front:\n";
            front_->print(os, indent + 1);
        } else {
            os << indentStr << "  Front: NULL\n";
        }
        
        // Back
        if (back_) {
            os << indentStr << "  Back:\n";
            back_->print(os, indent + 1);
        } else {
            os << indentStr << "  Back: NULL\n";
        }
    }


    // Recorrido
    void collectNodes(std::vector<const BSPNode<T>*>& nodes) const{
        nodes.push_back(this);
        if (front_)
            front_->collectNodes(nodes);
        if (back_)
            back_->collectNodes(nodes);
    }

    void collectPolygons(std::vector<Polygon<T>>& polys) const {
        polys.insert(polys.end(), polygons_.begin(), polygons_.end());
        if (front_)
            front_->collectPolygons(polys);
        if (back_)
            back_->collectPolygons(polys);
    }

    void traverse(std::function<void(const BSPNode<T>&)> func) const {
        func(*this);
        if (front_)
            front_->traverse(func);
        if (back_)
            back_->traverse(func);
    }
};

// BSPTree class template
template <typename T = NType>
class BSPTree {
private:
    std::unique_ptr<BSPNode<T>> root_;

public:
    BSPTree() : root_(nullptr) {}
    ~BSPTree() = default;

    void insert(const Polygon<T>& polygon){
        if (!root_) {
            root_ = std::make_unique<BSPNode<T>>();
            root_->insert(polygon);
            return;
        }
        root_->insert(polygon);
        return;

    }
    
    // Devuelve los polígonos candidatos a colisión con la Ball.
    std::vector<Polygon<T>> query(const Ball<T>& ball, const LineSegment<T>& movement) const{
        std::vector<Polygon<T>> results;
        std::vector<Polygon<T>> filter;
        if (root_) {
            root_->query(ball, movement, results);
        }

        for (auto it: results) {
            // get intersection point
            Plane<NType> plane = it.getPlane();
            NType d0 = plane.distance(movement.getP1());
            NType d1 = plane.distance(movement.getP2());
            NType denom = d0 - d1;
            if (denom == 0)
                continue;
            NType t = d0 / denom;
            if (t < NType(0) || t > NType(1))
                continue;

            Point3D<NType> intersection = movement.getP1() + (movement.getP2() - movement.getP1()) * t;
            if (it.contains(intersection)) {
                filter.push_back(it);
            }
        }
        return filter;
    }
    
    // Print
    void print(std::ostream& os) const{
        if (root_) {
            os << "BSPTree:\n";
            root_->print(os, 1); 
        } else {
            os << "BSPTree is empty.\n";
        }
    }


    // Funciones de recorrido
    std::vector<const BSPNode<T>*> getAllNodes() const{
        std::vector<const BSPNode<T>*> nodes;
        if (root_)
            root_->collectNodes(nodes);
        return nodes;
    }
    std::vector<Polygon<T>> getAllPolygons() const{
        std::vector<Polygon<T>> polys;
        if (root_)
            root_->collectPolygons(polys);
        return polys;
    }
    void traverse(std::function<void(const BSPNode<T>&)> func) const{
        if (root_)
            root_->traverse(func);
    }
};

#endif // BSPTREE_H
