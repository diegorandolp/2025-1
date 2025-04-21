#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>

class RNode;
typedef unsigned int  uint;
typedef unsigned char uchar;

class Point {
public:
    float x, y;
    Point() : x(0.0f), y(0.0f) {}
    Point(float x, float y) : x(x), y(y) {}

    // Distancia euclidiana
    float distanceTo(const Point &other) const {
        float dx = x - other.x;
        float dy = y - other.y;
        return std::sqrt(dx * dx + dy * dy);
    }
};


class MBB {
public:
    Point lower; // Esquina inferior izquierda
    Point upper; // Esquina superior derecha

    MBB() : lower(Point()), upper(Point()) {}
    MBB(const Point &p1, const Point &p2)
        : lower(Point(std::min(p1.x, p2.x), std::min(p1.y, p2.y))),
          upper(Point(std::max(p1.x, p2.x), std::max(p1.y, p2.y))) {}

    float area() const {
        float dx = upper.x - lower.x;
        float dy = upper.y - lower.y;
        return dx * dy;
    }
    float semiPerimeter() const {
        float dx = upper.x - lower.x;
        float dy = upper.y - lower.y;
        return dx + dy;
    }
    std::pair<float, float> min_distances_to_point(const Point &p) const {
        float dx_1 = std::max( p.x - upper.x, lower.x - p.x);
        float dx_2 = std::max(dx_1, 0.0f);
        float dy_1 = std::max(p.y - upper.y, lower.y - p.y);
        float dy_2 = std::max(dy_1, 0.0f);

        return std::make_pair(dx_2, dy_2);
    }
    float distanceTo(const Point &p) const {
        auto distances = min_distances_to_point(p);
        return std::sqrt(std::pow(distances.first, 2) + std::pow(distances.second, 2));
    }

    // Incremento del semiperimetro si agrega p
    float deltaSemiPerimeter(const Point &p) const {
        auto distances = min_distances_to_point(p);
        return distances.first + distances.second;
    }

    // Expande para incluir point o MBB
    void expandToInclude(const Point &p) {
        float dx_l = lower.x - p.x;
        float dx_r = p.x - upper.x;
        if (dx_l > 0){
            this->lower.x = this->lower.x - dx_l;
        } else if (dx_r > 0){
            this->upper.x = this->upper.x + dx_r;
        }

        float dy_l = lower.y - p.y;
        float dy_r = p.y - upper.y;
        if (dy_l > 0){
            this->lower.y = this->lower.y - dy_l;
        } else if (dy_r > 0){
            this->upper.y = this->upper.y + dy_r;
        }
    }

    void expandToInclude(const MBB &other) {
        expandToInclude(other.lower);
        expandToInclude(other.upper);
    }

    float intersectSegment(float thisLower, float thisUpper, float otherLower, float otherUpper) const{
        float bothLower = std::max(thisLower, otherLower);
        float bothUpper = std::min(thisUpper, otherUpper);
        float intersect = bothUpper - bothLower;
        if (intersect > 0){
            return intersect;
        }
        return 0.0f;
    }
    float intersects(const MBB &other) const{
        float dx = intersectSegment(lower.x, upper.x, other.lower.x, other.upper.x);
        float dy = intersectSegment(lower.y, upper.y, other.lower.y, other.upper.y);
        return dx * dy;
    }
    // Crear MBB a partir de un vector de puntos

    static MBB computeFromPoints(const std::vector<Point> &pts) {
        if (pts.empty())
            return MBB();
        Point lower = pts[0];
        Point upper = pts[0];
        for (const auto& point : pts) {
            if (point.x < lower.x)
                lower.x = point.x;
            if (point.y < lower.y)
                lower.y = point.y;
            if (point.x > upper.x)
                upper.x = point.x;
            if (point.y > upper.y)
                upper.y = point.y;
        }
        return MBB(lower, upper);
    }
    // Crear MBB a partir de un vector de nodos

    static MBB computeFromNodes(const std::vector<RNode*> &nodes);
    // Union MBBs
    static MBB unionOf(const MBB &a, const MBB &b) {
        MBB newMbb = MBB(a.lower, a.upper);
        newMbb.expandToInclude(b);
        return newMbb;
    }
};


// -------------------------------
// Clase RNode
// -------------------------------
class RNode {
private:
    // Linear Split para nodos hojas
    RNode* linearSplitLeaf(uchar maxEntries){
        if (points.size() <= maxEntries) {
            throw std::runtime_error("No deberia ocurrir esto(linearSplitLeaf");
        }
        int idx_p1 = 0;
        int idx_p2 = 0;
        // distance = 0
        float d = points[idx_p1].distanceTo(points[idx_p2]);

        // select points
        for (int i = 0; i < points.size(); i++){
            for (int j = i + 1; j < points.size(); j++){
                if(points[i].distanceTo(points[j]) > d){
                    idx_p1 = i;
                    idx_p2 = j;
                    d = points[i].distanceTo(points[j]);
                }
            }
        }
        // split
        std::vector<Point> points1;
        points1.push_back(points[idx_p1]);
        std::vector<Point> points2;
        points2.push_back(points[idx_p2]);

        MBB mbb1(points[idx_p1], points[idx_p1]);
        MBB mbb2(points[idx_p2], points[idx_p2]);

        for (int i = 0; i < points.size(); i++){
            if (i == idx_p1 || i == idx_p2){
                continue;
            }
            float dSemiPer1 = mbb1.deltaSemiPerimeter(points[i]);
            float dSemiPer2 = mbb2.deltaSemiPerimeter(points[i]);
            if (dSemiPer1 < dSemiPer2){
                points1.push_back(points[i]);
                mbb1.expandToInclude(points[i]);
            } else {
                points2.push_back(points[i]);
                mbb2.expandToInclude(points[i]);
            }
        }

        // create nodes
        this->isLeaf = true;
        this->mbr = mbb1;
        this->points = points1;
        RNode* node2 = new RNode(true);
        node2->mbr = mbb2;
        node2->points = points2;
        // return sibling
        return node2;
    }
    // Quadratic Split para nodos internos

    RNode* quadraticSplitInternal(uchar maxEntries){
        if (children.size() <= maxEntries){
            throw std::runtime_error("No deberia ocurrir esto(quadraticSplitInternal");
        }

        // choose groups
        int idx_n1 = 0;
        int idx_n2 = 0;
        float deadArea = 0;

        for (int i = 0; i < children.size(); i++){
            for (int j = i + 1; j < children.size(); j++){
                float newDeadArea = MBB::unionOf(children[i]->mbr, children[j]->mbr).area();
                // TODO: check if it is -intersect
                newDeadArea -= children[i]->mbr.area() + children[j]->mbr.area() - children[i]->mbr.intersects(children[j]->mbr);
                if (newDeadArea > deadArea){
                    deadArea = newDeadArea;
                    idx_n1 = i;
                    idx_n2 = j;
                }
            }
        }
        // divide
        std::vector<RNode*> node1;
        node1.push_back(children[idx_n1]);
        std::vector<RNode*> node2;
        node2.push_back(children[idx_n2]);
        MBB mbb1;
        mbb1 = MBB::computeFromNodes(node1);
        MBB mbb2;
        mbb2 = MBB::computeFromNodes(node2);
        for (int i = 0; i < children.size(); i++){
            if (i == idx_n1 || i == idx_n2){
                continue;
            }
            float dA1 = MBB::unionOf(mbb1, children[i]->mbr).area() - mbb1.area();
            float dA2 = MBB::unionOf(mbb2, children[i]->mbr).area() - mbb2.area();
            if (dA1 < dA2){
                mbb1.expandToInclude(children[i]->mbr);
                node1.push_back(children[i]);
            } else if (dA2 < dA1){
                mbb2.expandToInclude(children[i]->mbr);
                node2.push_back(children[i]);
            } else {
                float area1 = mbb1.area();
                float area2 = mbb2.area();
                if (area1 < area2){
                    mbb1.expandToInclude(children[i]->mbr);
                    node1.push_back(children[i]);
                } else {
                    mbb2.expandToInclude(children[i]->mbr);
                    node2.push_back(children[i]);
                }
            }
        }
        // replace
        this->mbr = mbb1;
        this->children = node1;

        RNode* newNode = new RNode(false);
        newNode->mbr = mbb2;
        newNode->children = node2;

        return newNode;

    }


    RNode* chooseNode(const Point &p){
        float dSemiPerimeter = std::numeric_limits<float>::max();
        int idx_n = -1;
        for (int i = 0; i < children.size(); i++){
            if (children[i] == nullptr)
                throw std::runtime_error("shouldnt happen (chooseNode)");
            if (children[i]->mbr.deltaSemiPerimeter(p) < dSemiPerimeter){
                dSemiPerimeter = children[i]->mbr.deltaSemiPerimeter(p);
                idx_n = i;
            } else if (children[i]->mbr.deltaSemiPerimeter(p) == dSemiPerimeter){
                float area1 = children[idx_n]->mbr.area();
                float area2 = children[i]->mbr.area();

                if (area1 > area2){

                    dSemiPerimeter = children[i]->mbr.deltaSemiPerimeter(p);
                    idx_n = i;

                }
            }
        }
        if (idx_n == -1)
            throw std::runtime_error("shouldnt happen (chooseNode)");
        return children[idx_n];

    }
public:
    bool isLeaf;
    MBB mbr;
    std::vector<Point>    points;
    std::vector<RNode*> children;

    RNode(bool leaf) : isLeaf(leaf) {}

    RNode* insert(const Point &p, uchar maxEntries) {
        if (isLeaf){
            if (points.empty())
                mbr = MBB(p, p);
            mbr.expandToInclude(p);
            points.push_back(p);
            if (points.size() <= maxEntries){
                return nullptr;
            } else {
                return this->linearSplitLeaf(maxEntries);
            }
        } else {
            mbr.expandToInclude(p);

            RNode* nodeToInsert = chooseNode(p);
            RNode* newChild = nodeToInsert->insert(p, maxEntries);

            // there is no overflow
            if (newChild == nullptr){
                return nullptr;
            } else { // there is overflow in leaf/internal node
                children.push_back(newChild);
                if (children.size() > maxEntries){
                    return this->quadraticSplitInternal(maxEntries);
                } else{
                    return nullptr;
                }
            }

        }
    };
    std::vector<Point> search(const MBB &query) const{
        std::vector<Point> pointsInArea;
        if (isLeaf) {
            for (auto point: points){
                if(query.distanceTo(point) == 0){
                    pointsInArea.push_back(point);
                }
            }
        } else {
            if (query.intersects(mbr) == 0 || children.empty()) {
                return pointsInArea;
            }
            for (int i = 0; i < children.size(); i++){
                if (children[i] == nullptr){
                    throw std::runtime_error("No deberia ocurrir (search)");
                }
                if(children[i]->mbr.intersects(query) > 0){
                    std::vector<Point> somePoints = children[i]->search(query);
                    for (auto point: somePoints){
                        pointsInArea.push_back(point);
                    }
                }
            }
        }
        return pointsInArea;
    }
};

MBB MBB::computeFromNodes(const std::vector<RNode*> &nodes){
        if (nodes.empty())
            return MBB();
        if (nodes[0] == nullptr)
            throw std::runtime_error("Nullptr in computeFromNodes");
        Point lower = nodes[0]->mbr.lower;
        Point upper = nodes[0]->mbr.upper;
        for (RNode* node: nodes){
            if (node == nullptr)
                throw std::runtime_error("Nullptr in computeFromNodes");
            if (node->mbr.lower.x < lower.x)
                lower.x = node->mbr.lower.x;
            if (node->mbr.lower.y < lower.y)
                lower.y = node->mbr.lower.y;
            if (node->mbr.upper.y > upper.y)
                upper.y = node->mbr.upper.y;
            if (node->mbr.upper.x > upper.x)
                upper.x = node->mbr.upper.x;
        }
        return MBB(lower, upper);

    }

// -------------------------------
// Para Best-First
// -------------------------------
struct QueueEntry {
    float distance;  // Distancia desde el query al MBB
    bool isNode;     // Si true, es un nodo; si false, es un punto
    RNode* node;
    Point pt;
};

struct QueueEntryComparator {
    bool operator()(const QueueEntry &a, const QueueEntry &b) const {
        return a.distance > b.distance;
    }
};

// -------------------------------
// Clase RTree
// -------------------------------
class RTree {
public:
    RNode* root;
    uchar maxEntries;  // Capacidad maxima

    RTree(uchar maxEntries = 3) : maxEntries(maxEntries) {
        root = new RNode(true);
    }

    void insert(const Point &p) {
        if (root == nullptr)
            throw std::runtime_error("shouldnt happen (insert rtrree)");
        RNode* newChild = root->insert(p, maxEntries);
        if (newChild != nullptr){ // overflow
            RNode* parent = new RNode(false);
            std::vector<RNode*> newChildren;
            newChildren.push_back(root);
            newChildren.push_back(newChild);
            // new mbr parent
            parent->mbr = MBB::computeFromNodes(newChildren);
            parent->children = newChildren;
            root = parent;
            return;
        }

    }
    std::vector<Point> search(const MBB &query) const {
        return root->search(query);
    }

    std::vector<Point> kNN(const Point &query, uchar k) const{

        if (k == 0 || !root)
            return std::vector<Point>();
        float furtherDistance = -1;
        std::priority_queue<QueueEntry, std::vector<QueueEntry>, QueueEntryComparator> minDistances;
        std::vector<QueueEntry> knns;
        QueueEntry entry;
        entry.distance = root->mbr.distanceTo(query);
        entry.isNode = true;
        entry.node = root;

        minDistances.push(entry);
        while(!minDistances.empty()){
             auto best = minDistances.top();
             minDistances.pop();
             if (best.isNode){
                if (best.node->isLeaf){
                    if (!best.node->points.empty()){
                        for(const Point &p: best.node->points){
                            QueueEntry entryPoint;
                            entryPoint.distance = query.distanceTo(p);
                            entryPoint.isNode = false;
                            entryPoint.pt = p;
                            entryPoint.node = nullptr;
                            minDistances.push(entryPoint);
                        }

                    }
                } else{ // intern node
                    if (!best.node->children.empty()){
                        for(RNode* n: best.node->children){
                            QueueEntry entryNode;
                            entryNode.distance = n->mbr.distanceTo(query);
                            entryNode.isNode = true;
                            entryNode.node = n;
                            minDistances.push(entryNode);
                        }

                    }
                }
             } else { // is Point
                knns.push_back(best);
                 if (best.distance > furtherDistance) {
                     furtherDistance = best.distance;
                 }
                if(knns.size() >= k){
                    if (minDistances.top().distance > furtherDistance){ // if the region is further than point, its done
                        break;
                    }
                }
             }
        }
        sort(knns.begin(), knns.end(), QueueEntryComparator());
        std::vector<Point> knns_point;
        for (int i = 0; i < knns.size(); i++){
            if (i > k-1){
               if(knns[i].distance == knns[k-1].distance) {
                    knns_point.push_back(knns[i].pt);
               } else {
                    break;
               }
            } else {
                knns_point.push_back(knns[i].pt);
            }
        }
        std::reverse(knns_point.begin(), knns_point.end());
        return knns_point;
    }
};
